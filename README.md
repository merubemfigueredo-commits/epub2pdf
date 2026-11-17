
# EPUB para PDF — Python + Streamlit

Aplicativo em português para enviar um arquivo `.epub`, escolher o formato de
página e baixar um PDF. O projeto funciona de forma independente: não depende
de React, Node.js, Replit, Calibre, chaves de API ou banco de dados.

## Recursos

- Upload de um EPUB de até 20 MB.
- Páginas A4, A5 ou Carta (Letter).
- Tamanho-base de fonte entre 9 e 18 pontos.
- Conversão com PyMuPDF, mantendo a ordem de leitura do EPUB.
- Download do PDF, metadados e quantidade de páginas.
- EPUB de exemplo original e download do código-fonte pela interface.
- Mensagens para arquivos inválidos, corrompidos, grandes ou com DRM.

## Executar no computador

Use **Python 3.12**. Na pasta que contém `app.py`:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Abra o endereço local informado pelo Streamlit. No Windows, dependendo da
instalação, substitua `python` por `py -3.12`.

## Criar seu repositório no GitHub

1. Extraia o ZIP recebido.
2. Entre no GitHub e crie um repositório, por exemplo `epub-para-pdf`.
3. Use **Add file → Upload files** para enviar os arquivos extraídos.
   Não envie somente o ZIP. `app.py` e `requirements.txt` devem estar na raiz
   do repositório.
4. Inclua a pasta `.streamlit` com `config.toml`, além de `converter.py`,
   `sample_book.py`, `README.md`, `NOTICE.md` e `.gitignore`.
   Se seu seletor esconder pastas iniciadas por ponto, crie o arquivo
   `.streamlit/config.toml` pelo editor do GitHub.
5. Salve as alterações com **Commit changes**.

Alternativa para quem usa Git (substitua a URL pela do seu repositório):

```bash
git init
git add .
git commit -m "Adiciona conversor EPUB para PDF"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/epub-para-pdf.git
git push -u origin main
```

## Publicar no Streamlit Community Cloud

1. Acesse https://share.streamlit.io/ e entre com sua conta.
2. Conecte sua conta do GitHub e autorize o acesso ao repositório.
3. Clique em **Create app** (ou **New app**, conforme a interface).
4. Escolha o repositório e a branch `main`.
5. Em **Main file path**, informe `app.py`.
6. Nas configurações avançadas, selecione **Python 3.12**.
7. Clique em **Deploy** e aguarde a instalação das dependências.

Não é necessário cadastrar secrets nem criar `packages.txt`. Se houver erro de
instalação, consulte os logs de gerenciamento do app e confira a versão do
Python e o conteúdo de `requirements.txt`.

Documentação oficial:
https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app

## Como usar

1. Se quiser testar sem um livro próprio, baixe o EPUB de exemplo na interface.
2. Envie esse arquivo ou outro EPUB sem DRM.
3. Escolha o papel e o tamanho-base da fonte.
4. Clique para converter; em seguida, use o botão de download do PDF.
5. Ao trocar o livro ou as opções, converta novamente. O resultado anterior
   não é apresentado como se correspondesse às opções novas.

## Estrutura

```text
app.py                   Interface Streamlit
converter.py             Validação e conversão em processo separado
sample_book.py           EPUB de exemplo gerado em memória
requirements.txt         Dependências Python
.streamlit/config.toml   Limite de upload e telemetria desativada
.gitignore               Ignora livros, PDFs e arquivos locais
NOTICE.md                Privacidade, direitos e licenças
README.md                Este guia
```

## Limitações e privacidade

EPUB é um formato de texto adaptável; PDF tem páginas fixas. Capas, imagens,
tabelas, fontes incorporadas, links e estilos complexos podem ficar diferentes.
O tamanho escolhido é a fonte-base: estilos do próprio livro podem prevalecer.
Não há garantia de reprodução idêntica, principalmente para EPUB de layout fixo.
Arquivos com DRM não são aceitos; o app não contorna proteções.

O limite descompactado é 80 MB, com até 4.000 entradas internas, 2.000 páginas
e 90 segundos por conversão. Livros grandes podem ultrapassar a memória
disponível na hospedagem mesmo dentro desses limites.

O processamento acontece **no servidor de hospedagem**, não somente no navegador.
O aplicativo não envia os livros a APIs de conversão e não mantém um histórico
persistente. O PDF é mantido na sessão para download; temporários são removidos
ao terminar a conversão, inclusive em erros tratados. Use a ação de limpar ou
encerre a sessão para descartar o resultado da interface. Não envie documentos
confidenciais a uma instância pública sem avaliar a política da hospedagem.

O subprocesso limita o tempo de conversão, mas não substitui isolamento de
segurança e limites de memória para um serviço público de produção.

## Licenciamento

Leia `NOTICE.md`, especialmente as condições AGPL/comerciais do PyMuPDF, antes
de redistribuir ou incorporar o conversor em um produto fechado.
