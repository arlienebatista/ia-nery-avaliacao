# Publicar o app na web e gravar no Google Sheets

São duas coisas independentes. Você pode fazer só a primeira (o app grava em CSV
local), só a segunda (rodando na sua máquina, mas gravando no Sheets), ou as
duas. Para uma avaliação remota de verdade, faça as duas: no Streamlit Cloud o
disco é apagado a cada reinício, então o CSV local **não** é destino confiável lá.

---

# Parte 1: gravar no Google Sheets

## 1. Criar a planilha de respostas

No Google Drive, crie uma planilha nova, por exemplo `Respostas Avaliacao Nery`.
Não precisa criar colunas nem abas: o app cria a aba `respostas` com o cabeçalho
na primeira gravação. Guarde a URL dela.

## 2. Criar a conta de serviço

Uma conta de serviço é um "usuário robô" que o app usa para escrever na planilha,
sem envolver a sua conta pessoal do Google.

1. Acesse <https://console.cloud.google.com/> e faça login.
2. No seletor de projetos, no topo, clique em **Novo projeto**. Nome sugerido:
   `avaliacao-nery`. Crie e espere selecionar o projeto.
3. Menu lateral > **APIs e serviços** > **Biblioteca**. Procure e ative estas
   duas APIs, uma de cada vez: **Google Sheets API** e **Google Drive API**.
4. Menu lateral > **APIs e serviços** > **Credenciais** > **Criar credenciais** >
   **Conta de serviço**. Nome: `app-avaliacao`. Pode pular as etapas opcionais de
   permissão e concluir.
5. Na lista de contas de serviço, clique na que você criou > aba **Chaves** >
   **Adicionar chave** > **Criar nova chave** > tipo **JSON** > **Criar**. Um
   arquivo `.json` é baixado. **Esse arquivo é uma senha: não coloque no
   GitHub e não envie por e-mail.**

## 3. Dar acesso da planilha à conta de serviço

Abra o `.json` baixado e copie o valor do campo `client_email` (algo como
`app-avaliacao@avaliacao-nery.iam.gserviceaccount.com`). Na sua planilha de
respostas, clique em **Compartilhar** e adicione esse e-mail como **Editor**.

Sem esse passo, o app não consegue escrever, e a barra lateral vai continuar
mostrando que está gravando no arquivo local.

## 4. Configurar o app

Crie o arquivo `.streamlit/secrets.toml` dentro da pasta do projeto, com este
conteúdo, preenchido a partir do `.json` baixado:

```toml
[planilha]
url = "https://docs.google.com/spreadsheets/d/COLE_O_ID_AQUI/edit"
aba = "respostas"

[gcp_service_account]
type = "service_account"
project_id = "avaliacao-nery"
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\nMIIE...\n-----END PRIVATE KEY-----\n"
client_email = "app-avaliacao@avaliacao-nery.iam.gserviceaccount.com"
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
universe_domain = "googleapis.com"
```

Dois cuidados com a `private_key`: ela vai entre aspas normais, numa linha só, e
os `\n` do arquivo JSON devem ser mantidos exatamente como estão.

O arquivo `.gitignore` deste projeto já ignora `.streamlit/secrets.toml`, para
ele não subir para o GitHub por acidente.

## 5. Conferir

Rode `streamlit run app.py`. Na barra lateral deve aparecer
**"Gravando em: Google Sheets"**. Se aparecer o arquivo local, a barra lateral
mostra logo abaixo o motivo da falha (credencial inválida, planilha não
compartilhada, API não ativada).

---

# Parte 2: publicar no Streamlit Community Cloud

É gratuito e exige uma conta no GitHub. O repositório precisa ser **público**, ou
seja, as perguntas, as respostas da Nery e os trechos dos manuais ficam visíveis
para quem encontrar o repositório. As respostas dos juízes **não** ficam: elas
vão para a sua planilha privada. Se a exposição desses textos for um problema
antes da defesa, pule para a seção de alternativas no fim.

## 1. Subir o projeto para o GitHub

Crie um repositório novo em <https://github.com/new>, por exemplo
`avaliacao-nery`, e depois, dentro da pasta do projeto:

```bash
git init && git add . && git commit -m "Interface de avaliacao da Nery"
```

```bash
git remote add origin https://github.com/SEU_USUARIO/avaliacao-nery.git && git branch -M main && git push -u origin main
```

Antes do push, confirme que o `secrets.toml` não está incluído:

```bash
git status --porcelain | grep secrets
```

Se esse comando imprimir alguma coisa, pare e verifique o `.gitignore`.

## 2. Criar o app

1. Acesse <https://share.streamlit.io/> e entre com o GitHub.
2. **Create app** > **Deploy a public app from GitHub**.
3. Repositório: o que você acabou de criar. Branch: `main`. Main file path:
   `app.py`.
4. Antes de clicar em Deploy, abra **Advanced settings** > **Secrets** e cole ali
   o mesmo conteúdo do seu `.streamlit/secrets.toml`. É assim que a credencial
   chega ao servidor sem passar pelo GitHub.
5. **Deploy**. Em um ou dois minutos você recebe uma URL como
   `https://avaliacao-nery.streamlit.app`. É essa URL que você manda aos juízes.

## 3. Detalhes de operação

- **Hibernação:** apps sem acesso por alguns dias hibernam e a primeira abertura
  demora uns segundos. Se você mesma abrir a URL na véspera do envio aos juízes,
  eles já pegam o app acordado.
- **Atualizar as questões:** edite o `questoes.csv`, faça commit e push. O app
  redeploya sozinho em cerca de um minuto.
- **Trocar a credencial depois:** no painel do app, menu de três pontos >
  **Settings** > **Secrets**.
- **Vários juízes ao mesmo tempo:** funciona. Cada um tem sua própria sessão, e
  a gravação é por linha, então não há risco de um sobrescrever o outro.

---

# Alternativas ao Streamlit Cloud

**Hugging Face Spaces** (<https://huggingface.co/new-space>, SDK Streamlit): mesmo
esquema, e permite Space privado, mas aí cada juiz precisa de conta na
plataforma. Os secrets vão em Settings > Variables and secrets.

**Rodar na sua máquina para um juiz por vez:** `streamlit run app.py` e
compartilhamento de tela, ou o juiz avalia no seu computador. Sem exposição
nenhuma dos textos, mas sem conveniência remota.
