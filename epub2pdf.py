"""EPUB para PDF - interface Streamlit."""

from __future__ import annotations

import hashlib
import re
import zipfile
from io import BytesIO
from pathlib import Path

import streamlit as st

from converter import MAX_UPLOAD_MB, ConversionError, convert_epub
""" from sample_book import create_sample_epub """

BASE_DIR = Path(__file__).parent
SOURCE_FILES = [
    "app.py",
    "converter.py",
    "sample_book.py",
    "requirements.txt",
    "README.md",
    ".gitignore",
    ".streamlit/config.toml",
    "NOTICE.md",
]
PAGE_SIZES = ["A4", "A5", "Letter"]
MAX_BYTES = MAX_UPLOAD_MB * 1024 * 1024

st.set_page_config(page_title="EPUB para PDF", page_icon=None, layout="centered")

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0
if "result" not in st.session_state:
    st.session_state.result = None
if "result_key" not in st.session_state:
    st.session_state.result_key = None


def build_source_zip() -> bytes:
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel in SOURCE_FILES:
            path = BASE_DIR / rel
            if path.is_file():
                zf.write(path, arcname=rel)
    return buffer.getvalue()


def safe_filename(title: str) -> str:
    name = re.sub(r"[^\w\- ]+", "", title or "", flags=re.UNICODE).strip()
    name = re.sub(r"\s+", "-", name)[:80]
    return (name or "livro") + ".pdf"


def clear_result() -> None:
    st.session_state.result = None
    st.session_state.result_key = None
    st.session_state.uploader_key += 1


st.title("EPUB para PDF")
st.write(
    "Transforme seus próprios livros EPUB em PDFs prontos para imprimir ou ler "
    "em qualquer dispositivo, sem enviar o arquivo a serviços externos de conversão."
)

tab_convert, tab_help, tab_source = st.tabs(["Converter", "Como funciona", "Código-fonte"])

with tab_convert:
    uploaded = st.file_uploader(
        "Escolha um arquivo EPUB",
        type=["epub"],
        key=f"uploader_{st.session_state.uploader_key}",
        help=f"Tamanho máximo: {MAX_UPLOAD_MB} MB.",
    )

    col1, col2 = st.columns(2)
    with col1:
        page_size = st.selectbox("Tamanho da página", PAGE_SIZES, index=0)
    with col2:
        font_size = st.slider("Tamanho da fonte (pt)", min_value=9, max_value=18, value=12)

    if uploaded is None:
        st.session_state.result = None
        st.session_state.result_key = None
        st.info(
            "Envie um arquivo EPUB para começar."         
        )
    """    st.download_button(
            "Baixar EPUB de exemplo",
            data=create_sample_epub(),
            file_name="livro-exemplo.epub",
            mime="application/epub+zip",
        ) """
    else: 
        data = uploaded.getvalue() 
        if len(data) > MAX_BYTES:
            st.error(
                f"Este arquivo tem {len(data) / (1024 * 1024):.1f} MB e ultrapassa o "
                f"limite de {MAX_UPLOAD_MB} MB. Escolha um arquivo menor."
            )
        else:
            current_key = f"{hashlib.sha256(data).hexdigest()}:{page_size}:{font_size}"
            if st.session_state.result_key != current_key:
                st.session_state.result = None

            if st.session_state.result is None:
                st.caption(
                    f"Arquivo: {uploaded.name} ({len(data) / 1024:.0f} KB) - "
                    f"página {page_size}, fonte {font_size} pt"
                )
                if st.button("Converter para PDF", type="primary", use_container_width=True):
                    try:
                        with st.spinner("Convertendo seu livro. Isso pode levar alguns instantes..."):
                            result = convert_epub(data, page_size=page_size, font_size=font_size)
                        st.session_state.result = result
                        st.session_state.result_key = current_key
                        st.rerun()
                    except ConversionError as exc:
                        st.error(f"Não foi possível converter este livro: {exc}")
                    except Exception:
                        st.error(
                            "Ocorreu um erro inesperado durante a conversão. Verifique se o "
                            "arquivo é um EPUB válido e sem DRM e tente novamente."
                        )

            result = st.session_state.result
            if result is not None:
                st.success("Conversão concluída. Seu PDF está pronto.")
                with st.container(border=True):
                    st.subheader(result.title or "Sem título")
                    st.write(f"Autor: {result.author or 'Desconhecido'}")
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Páginas", result.pages)
                    m2.metric("Formato", page_size)
                    m3.metric("Fonte", f"{font_size} pt")
                st.download_button(
                    "Baixar PDF",
                    data=result.pdf,
                    file_name=safe_filename(result.title),
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True,
                )
                if st.button("Limpar e converter outro livro", use_container_width=True):
                    clear_result()
                    st.rerun()

with tab_help:
    st.subheader("Passo a passo")
    st.markdown(
        "1. Envie um arquivo `.epub` de sua propriedade.\n"
        "2. Escolha o tamanho da página (A4, A5 ou Letter) e o tamanho da fonte.\n"
        "3. Clique em **Converter para PDF** e aguarde.\n"
        "4. Baixe o PDF gerado. Se mudar o arquivo ou as opções, converta novamente."
    )
    st.subheader("Privacidade")
    st.markdown(
        "- O arquivo é processado no servidor que hospeda este aplicativo, e não "
        "localmente no seu navegador.\n"
        "- Ele não é repassado a serviços externos de conversão.\n"
        "- Os dados ficam apenas em memória e em diretórios temporários usados durante "
        "a conversão; nada é guardado em histórico.\n"
        "- Para total controle, baixe o código-fonte e rode o aplicativo no seu computador."
    )
    st.subheader("Limitações")
    st.markdown(
        f"- Livros protegidos por DRM não são suportados.\n"
        f"- Layouts complexos (tabelas elaboradas, layout fixo, fontes embutidas, "
        f"scripts) podem ficar diferentes do original.\n"
        f"- Tamanho máximo do arquivo: {MAX_UPLOAD_MB} MB."
    )
    st.warning("Converta apenas livros que você tem o direito de usar.")

with tab_source:
    st.subheader("Baixe o código-fonte")
    st.write(
        "O pacote contém tudo o que é necessário para rodar o aplicativo localmente "
        "ou publicá-lo no Streamlit Community Cloud."
    )
    st.code("pip install -r requirements.txt\nstreamlit run app.py", language="bash")
    st.download_button(
        "Baixar código-fonte (.zip)",
        data=build_source_zip(),
        file_name="epub-para-pdf.zip",
        mime="application/zip",
    )
