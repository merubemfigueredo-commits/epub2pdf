# EPUB para PDF — Python + Streamlit

Aplicativo em português para enviar um arquivo `.epub`, escolher o formato de
página e baixar um PDF. O projeto funciona de forma independente: não depende
de React, Node.js, Replit, Calibre, chaves de API ou banco de dados.

## Recursos

- Upload de um EPUB de até 50 MB por arquivo.
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

### Atualizar o limite para 50 MB

O pacote para download inclui `epub2pdf.py` (sem botão de livro de exemplo)
e `app.py` (com o botão de exemplo). Use apenas um deles como arquivo principal.
Para atualizar um deploy que já utiliza `epub2pdf.py`, mantenha esse nome em
**Main file path** e envie os arquivos extraídos deste pacote para o GitHub.
Não envie apenas o ZIP.

Atualize principalmente `epub2pdf.py`, `converter.py` e
`.streamlit/config.toml`, mantendo também as dependências e demais arquivos
do pacote. Faça o commit na branch usada pelo Cloud e reinicie o app.

O limite de **50 MB** é aplicado no campo de upload e nas duas verificações
do conversor. O campo usa explicitamente `max_upload_size=MAX_UPLOAD_MB`,
para não voltar a mostrar o padrão de 200 MB se a pasta `.streamlit` ficar
fora do envio. O arquivo de configuração também declara:

```toml
[server]
headless = true
maxUploadSize = 50

[browser]
gatherUsageStats = false
```

O tamanho é medido em blocos de 1.024 × 1.024 bytes: o limite efetivo é
52.428.800 bytes. Um arquivo de 23,4 MB não será recusado pelo limite de upload.
Ainda poderá ser recusado por estrutura inválida, DRM, expansão excessiva
ou pelos outros limites de segurança.

Documentação oficial:
https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app

### Corrigir `ModuleNotFoundError: No module named 'defusedxml'`

Esse erro significa que a dependência de validação segura de XML não foi
instalada no ambiente do app. Ela é necessária; não remova o import nem
substitua por um parser sem proteção.

1. Envie o `requirements.txt` deste pacote para o GitHub, na mesma pasta do
   arquivo principal. O nome deve ser exatamente `requirements.txt`, não
   `requirements.txt.txt`. Confirme que ele contém:

   ```text
   streamlit==1.67.0
   PyMuPDF==2.1
   defusedxml==0.7.1
   ```

2. Se você renomeou `app.py` para `epub2pdf.py`, pode manter esse nome:
   deixe `converter.py`, `sample_book.py` e `requirements.txt` ao lado dele
   e use `epub2pdf.py` em **Main file path**. A renomeação não causa esse erro.
3. Confirme que o app no Streamlit Cloud usa a mesma branch em que você
   salvou o arquivo. Se há outro manifesto de dependências, como `uv.lock`,
   `Pipfile` ou `environment.yml`, verifique nos logs qual está sendo usado:
   as dependências também precisam estar declaradas nele, ou publique este
   pacote independente usando somente o `requirements.txt`.
4. Faça **Commit changes**, aguarde a reinstalação e, se necessário,
   use **Manage app → Reboot app** no Streamlit Cloud.
5. Nos logs de instalação, confirme a instalação de `defusedxml`. Se ela
   continuar ausente, confira novamente a branch, a pasta e o manifesto
   escolhido pelo Cloud. Não tente instalar pacotes de dentro de `app.py`.

Organização válida para o arquivo principal renomeado:

```text
epub2pdf.py
converter.py
sample_book.py
requirements.txt
.streamlit/config.toml
```

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
epub2pdf.py              Interface sem botão de exemplo, incluída no ZIP atualizado
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

O limite de upload é 50 MB. O limite descompactado continua em 80 MB, com até
4.000 entradas internas, 2.000 páginas
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
