# Avisos e licenças

- Converta apenas livros que você tenha direito de usar e converter.
- O aplicativo não remove DRM.
- PyMuPDF/MuPDF é oferecido sob AGPL e licença comercial. Antes de redistribuir
  ou usar este projeto em um produto fechado, confira as condições da versão
  utilizada em https://pymupdf.readthedocs.io/en/latest/about.html#license-and-copyright
  e https://artifex.com/licensing/. Manter um repositório público não substitui
  a leitura e o cumprimento da licença.
- Streamlit e defusedxml têm suas próprias licenças, incluídas nos respectivos
  pacotes. Os avisos originais dessas dependências devem ser preservados.
- O livro de exemplo é um texto e uma ilustração originais deste projeto,
  disponibilizados sob CC0 para testes.
- O servidor recebe o EPUB para processá-lo. Não há serviço externo de conversão
  nem banco de dados de livros. Uploads e resultados ficam na memória da sessão;
  arquivos temporários são criados durante a conversão e removidos ao término
  normal, erro tratado ou timeout. Encerramentos abruptos do servidor podem
  deixar temporários até a limpeza do ambiente.
- Limites de tamanho, quantidade de entradas, páginas e tempo reduzem riscos,
  mas não constituem uma sandbox de segurança. Para um serviço público com
  grande tráfego ou arquivos não confiáveis, use isolamento adicional e
  controle de recursos no ambiente de hospedagem.
