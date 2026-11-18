"""A small original EPUB for trying the app without copyrighted material."""

from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED


def create_sample_epub() -> bytes:
    output = BytesIO()
    files = {
        "META-INF/container.xml": """<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
<rootfiles><rootfile full-path="OEBPS/content.opf"
media-type="application/oebps-package+xml"/></rootfiles></container>""",
        "OEBPS/content.opf": """<?xml version="1.0" encoding="UTF-8"?>
<package version="3.0" unique-identifier="id" xmlns="http://www.idpf.org/2007/opf">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="id">urn:uuid:epub-pdf-exemplo-original</dc:identifier>
<dc:title>Uma pausa para ler</dc:title><dc:creator>Projeto EPUB para PDF</dc:creator>
<dc:language>pt-BR</dc:language>
<meta property="dcterms:modified">2026-01-01T00:00:00Z</meta></metadata>
<manifest><item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
<item id="c1" href="chapter1.xhtml" media-type="application/xhtml+xml"/>
<item id="c2" href="chapter2.xhtml" media-type="application/xhtml+xml"/>
<item id="art" href="illustration.svg" media-type="image/svg+xml"/></manifest>
<spine><itemref idref="c1"/><itemref idref="c2"/></spine></package>""",
        "OEBPS/nav.xhtml": """<html xmlns="http://www.w3.org/1999/xhtml"
xmlns:epub="http://www.idpf.org/2007/ops" lang="pt-BR">
<head><title>Sumário</title></head><body><nav epub:type="toc"><ol>
<li><a href="chapter1.xhtml">O primeiro capítulo</a></li>
<li><a href="chapter2.xhtml">Leitura em qualquer lugar</a></li>
</ol></nav></body></html>""",
        "OEBPS/chapter1.xhtml": """<html xmlns="http://www.w3.org/1999/xhtml" lang="pt-BR">
<head><title>O primeiro capítulo</title></head><body>
<h1>Uma pausa para ler</h1><h2>O primeiro capítulo</h2>
<p>Um livro começa com um convite: reserve um momento para descobrir algo novo.</p>
<p>Esta é uma amostra original para experimentar a conversão de EPUB para PDF.
Acentos também fazem parte da história: ação, coração, café, São Paulo.</p>
<p><strong>Textos em destaque</strong> e <em>palavras em itálico</em>
ajudam a organizar a leitura.</p>
<img src="illustration.svg" alt="Um livro aberto" width="240" height="120"/>
</body></html>""",
        "OEBPS/chapter2.xhtml": """<html xmlns="http://www.w3.org/1999/xhtml" lang="pt-BR">
<head><title>Leitura em qualquer lugar</title></head><body>
<h1>Leitura em qualquer lugar</h1>
<p>No EPUB, o texto se adapta à tela. No PDF, cada página tem um tamanho fixo.</p>
<p>Por isso, a quantidade de páginas pode mudar quando você ajusta o papel
ou a fonte. O conteúdo continua seguindo a ordem dos capítulos.</p>
<ul><li>Escolha o formato de página.</li><li>Ajuste o tamanho-base da fonte.</li>
<li>Converta e baixe seu PDF.</li></ul>
<p>Boa leitura!</p></body></html>""",
        "OEBPS/illustration.svg": """<svg xmlns="http://www.w3.org/2000/svg" width="240" height="120">
<rect width="240" height="120" fill="#f3ede1"/>
<path d="M30 25 Q75 10 120 30 Q165 10 210 25 V95 Q165 80 120 100
Q75 80 30 95Z" fill="#ffffff" stroke="#556855" stroke-width="3"/>
<path d="M120 30V100" stroke="#556855" stroke-width="3"/></svg>""",
    }
    with ZipFile(output, "w") as archive:
        archive.writestr("mimetype", "application/epub+zip", compress_type=ZIP_STORED)
        for path, content in files.items():
            archive.writestr(path, content.encode("utf-8"), compress_type=ZIP_DEFLATED)
    return output.getvalue()
