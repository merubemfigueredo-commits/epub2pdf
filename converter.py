"""EPUB conversion with bounded input and a separate, time-limited worker.

No Calibre, browser engine, API key, or system package is required.
"""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
from tempfile import TemporaryDirectory
from urllib.parse import unquote
from zipfile import BadZipFile, ZipFile

from defusedxml import ElementTree
from defusedxml.common import DefusedXmlException

MAX_UPLOAD_MB = 20
MAX_EXPANDED_BYTES = 80 * 1024 * 1024
MAX_ENTRIES = 4000
MAX_PAGES = 2000
TIMEOUT_SECONDS = 90
PAGE_SIZES = {"A4": (595, 842), "A5": (420, 595), "Letter": (612, 792)}


class ConversionError(ValueError):
    """A conversion failure that may be displayed to the reader."""


@dataclass(frozen=True)
class ConversionResult:
    pdf: bytes
    title: str
    author: str
    pages: int


def validate_epub(data: bytes) -> None:
    """Check the container without extracting any user-supplied paths."""
    if not data:
        raise ConversionError("O arquivo está vazio. Escolha um EPUB válido.")
    if len(data) > MAX_UPLOAD_MB * 1024 * 1024:
        raise ConversionError(f"O limite é de {MAX_UPLOAD_MB} MB por arquivo.")
    try:
        with ZipFile(BytesIO(data)) as archive:
            entries = archive.infolist()
            if len(entries) > MAX_ENTRIES:
                raise ConversionError("Este EPUB contém arquivos internos demais.")
            if sum(e.file_size for e in entries) > MAX_EXPANDED_BYTES:
                raise ConversionError("O EPUB descompactado excede o limite de 80 MB.")
            names = [e.filename for e in entries]
            if len(names) != len(set(names)):
                raise ConversionError("O EPUB contém entradas duplicadas e é inválido.")
            for entry in entries:
                path = PurePosixPath(entry.filename)
                if path.is_absolute() or ".." in path.parts or "\\" in entry.filename:
                    raise ConversionError("O EPUB contém caminhos internos inválidos.")
                if entry.flag_bits & 1:
                    raise ConversionError("Arquivos EPUB criptografados não são aceitos.")
                if entry.file_size > 1024 * 1024 and (
                    entry.file_size / max(entry.compress_size, 1) > 250
                ):
                    raise ConversionError("O EPUB tem uma taxa de compressão insegura.")
            if archive.read("mimetype").strip() != b"application/epub+zip":
                raise ConversionError("O arquivo não é um EPUB válido.")
            container = ElementTree.fromstring(archive.read("META-INF/container.xml"))
            rootfiles = container.findall(".//{*}rootfile")
            if not rootfiles:
                raise ConversionError("Não foi possível localizar o conteúdo do livro.")
            package_path = unquote(rootfiles[0].get("full-path", ""))
            if not package_path or package_path not in names:
                raise ConversionError("O índice de conteúdo do EPUB está ausente.")
            package = ElementTree.fromstring(archive.read(package_path))
            if package.find(".//{*}spine") is None:
                raise ConversionError("O EPUB não informa a ordem de leitura.")
            if "META-INF/encryption.xml" in names:
                encryption = ElementTree.fromstring(
                    archive.read("META-INF/encryption.xml")
                )
                # Standard font obfuscation is not book DRM.
                font_obfuscation = {
                    "http://www.idpf.org/2008/embedding",
                    "http://ns.adobe.com/pdf/enc#RC",
                }
                for method in encryption.findall(".//{*}EncryptionMethod"):
                    if method.get("Algorithm") not in font_obfuscation:
                        raise ConversionError(
                            "Este EPUB tem proteção DRM. Utilize uma cópia sem DRM "
                            "que você tenha direito de converter."
                        )
    except ConversionError:
        raise
    except (BadZipFile, KeyError, RuntimeError, OSError, ValueError,
            ElementTree.ParseError, DefusedXmlException, NotImplementedError) as exc:
        raise ConversionError(
            "O arquivo está danificado ou não possui uma estrutura EPUB válida."
        ) from exc


def _render(data: bytes, page_size: str, font_size: int) -> ConversionResult:
    import pymupdf

    validate_epub(data)
    width, height = PAGE_SIZES[page_size]
    try:
        with pymupdf.open(stream=data, filetype="epub") as book:
            book.layout(rect=pymupdf.Rect(0, 0, width, height), fontsize=font_size)
            if book.page_count < 1:
                raise ConversionError("O EPUB não contém páginas legíveis.")
            if book.page_count > MAX_PAGES:
                raise ConversionError(
                    "O resultado ultrapassaria 2.000 páginas. Tente uma fonte menor."
                )
            metadata = book.metadata or {}
            title = metadata.get("title") or "Livro convertido"
            author = metadata.get("author") or "Autor não informado"
            toc = book.get_toc()
            raw_pdf = book.convert_to_pdf()
        with pymupdf.open(stream=raw_pdf, filetype="pdf") as pdf:
            pdf.set_metadata({
                "title": title,
                "author": metadata.get("author") or "",
                "subject": metadata.get("subject") or "",
                "creator": "EPUB para PDF — Python e Streamlit",
            })
            if toc:
                pdf.set_toc(toc)
            return ConversionResult(
                pdf=pdf.tobytes(garbage=4, deflate=True),
                title=title,
                author=author,
                pages=pdf.page_count,
            )
    except ConversionError:
        raise
    except Exception as exc:
        raise ConversionError(
            "Não foi possível converter este EPUB. Ele pode estar protegido, "
            "danificado ou usar recursos não suportados."
        ) from exc


def convert_epub(
    data: bytes, page_size: str = "A4", font_size: int = 12
) -> ConversionResult:
    """Run conversion out of the UI process; remove temporary files on exit."""
    if page_size not in PAGE_SIZES:
        raise ConversionError("Escolha A4, A5 ou Letter.")
    if type(font_size) is not int or not 9 <= font_size <= 18:
        raise ConversionError("O tamanho da fonte deve estar entre 9 e 18.")
    if not data or len(data) > MAX_UPLOAD_MB * 1024 * 1024:
        raise ConversionError(f"Escolha um EPUB não vazio de até {MAX_UPLOAD_MB} MB.")
    with TemporaryDirectory(prefix="epub-pdf-") as temp:
        folder = Path(temp)
        (folder / "book.epub").write_bytes(data)
        try:
            process = subprocess.run(
                [sys.executable, str(Path(__file__).resolve()), "--worker",
                 str(folder), page_size, str(font_size)],
                capture_output=True,
                timeout=TIMEOUT_SECONDS,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise ConversionError(
                "A conversão excedeu 90 segundos. Tente um livro menor."
            ) from exc
        except OSError as exc:
            raise ConversionError("Não foi possível iniciar a conversão.") from exc
        if process.returncode != 0 or not (folder / "result.json").exists():
            raise ConversionError(
                "O conversor foi interrompido. Tente um livro menor ou outro EPUB."
            )
        info = json.loads((folder / "result.json").read_text(encoding="utf-8"))
        if "error" in info:
            raise ConversionError(info["error"])
        return ConversionResult(pdf=(folder / "book.pdf").read_bytes(), **info)


def _worker() -> None:
    folder, page_size, font_size = Path(sys.argv[2]), sys.argv[3], int(sys.argv[4])
    try:
        result = _render((folder / "book.epub").read_bytes(), page_size, font_size)
        (folder / "book.pdf").write_bytes(result.pdf)
        info = {"title": result.title, "author": result.author, "pages": result.pages}
    except ConversionError as exc:
        info = {"error": str(exc)}
    (folder / "result.json").write_text(
        json.dumps(info, ensure_ascii=False), encoding="utf-8"
    )


if __name__ == "__main__" and len(sys.argv) == 5 and sys.argv[1] == "--worker":
    _worker()
