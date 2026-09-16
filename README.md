# Julius

Julius monitora novas mensagens em canais do Telegram e envia um alerta por bot quando encontra uma das palavras-chave configuradas. O alerta contém a palavra encontrada, o nome do canal e o texto da mensagem.

A leitura dos canais usa sua conta do Telegram, conectada pelo Telethon. O bot é usado para enviar os alertas.

## 1. Preparar o ambiente

Você precisa de Python 3.10 ou superior, acesso à internet e uma conta do Telegram que faça parte dos canais monitorados.

Baixe ou clone este projeto e abra um terminal na pasta que contém `julius.py`. Crie e ative um ambiente virtual:

**Linux ou macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Com o ambiente ativado, instale as dependências:

```bash
python -m pip install telethon python-dotenv requests
```

## 2. Configurar as credenciais

Renomeie ou copie [`.env-exemplo`](.env-exemplo) para `.env` na pasta do projeto:

**Linux ou macOS:**

```bash
cp .env-exemplo .env
```

**Windows (PowerShell):**

```powershell
Copy-Item .env-exemplo .env
```



### Obter API_ID e API_HASH

Entre em [my.telegram.org](https://my.telegram.org), abra **API development tools** e cadastre uma aplicação. Copie o `api_id` e o `api_hash` para o `.env`, conforme o [guia oficial do Telegram](https://core.telegram.org/api/obtaining_api_id).

### Criar o bot

Converse com o [@BotFather](https://t.me/BotFather), envie `/newbot` e siga as instruções. Salve o token recebido em `BOT_TOKEN`. Abra uma conversa com o bot criado e envie `/start`. Veja o [tutorial oficial de criação de bots](https://core.telegram.org/bots/tutorial).

### Descobrir o CHAT_ID

Para receber os alertas na conversa privada com seu bot:

1. Envie uma mensagem ao bot, como `/start`.
2. Abra a URL abaixo, substituindo `<BOT_TOKEN>` pelo token recebido:
  ```text
   https://api.telegram.org/bot<BOT_TOKEN>/getUpdates
  ```
3. Na resposta, encontre `result` → uma atualização → `message` → `chat` → `id`.
4. Copie esse número para `CHAT_ID` no `.env`.

Se `result` estiver vazio, envie outra mensagem ao bot e consulte novamente. Esse procedimento usa o método oficial [getUpdates](https://core.telegram.org/bots/api#getupdates); ele não funciona enquanto o bot tiver um webhook configurado.

## 3. Escolher palavras-chave e canais

Edite as listas no arquivo [`julius.py`](julius.py).

Em `ALVOS`, coloque as palavras ou expressões que deseja acompanhar:

```python
ALVOS = [
    "notebook",
    "fone de ouvido",
    "ar condicionado",
]
```

A busca ignora diferenças entre maiúsculas, minúsculas e acentos. Espaços e hífens entre as partes de uma palavra-chave podem aparecer ou ser omitidos na mensagem:


| Palavra-chave cadastrada | Exemplos reconhecidos                                  |
| ------------------------ | ------------------------------------------------------ |
| `ar condicionado`        | `ar condicionado`, `ar-condicionado`, `arcondicionado` |
| `fone de ouvido`         | `fone de ouvido`, `fone-de-ouvido`, `fonedeouvido`     |
| `café`                   | `café`, `cafe`, `CAFÉ`                                 |


Cadastre expressões compostas com espaços ou hífens para indicar onde a separação pode variar. Cadastrar apenas `arcondicionado` não permite deduzir a separação em `ar condicionado`.

A busca respeita os limites das palavras: `notebook` não corresponde a `notebooks`. Se a mensagem tiver mais de uma palavra-chave, o alerta informa a primeira encontrada na ordem de `ALVOS`.

Em `CANAIS`, substitua os exemplos pelos nomes de usuário dos canais desejados:

```python
CANAIS = [
    "@nome_do_canal",
    "@outro_canal",
]
```

Entre nesses canais com a conta que você usará para autenticar o Julius. Não deixe os nomes fictícios do exemplo na configuração.

## 4. Executar

Na pasta do projeto, com o ambiente virtual ativado, execute:

```bash
python julius.py
```

No primeiro acesso, informe seu telefone com código do país, o código de login solicitado pelo Telegram e, se habilitada, sua senha de verificação em duas etapas.

O Telethon salva o login em `sessao_filtro.session`, permitindo reutilizar a sessão nas próximas execuções. O terminal exibe `Julius está trabalhando...`; conclua o login caso ele ainda seja solicitado.

Mantenha o processo em execução para acompanhar novas mensagens. O programa não faz uma busca no histórico dos canais. Para encerrar, pressione `Ctrl+C`. Depois de alterar palavras-chave, canais ou credenciais, reinicie o programa.

Para verificar o funcionamento, publique uma nova mensagem com uma palavra-chave em um canal configurado no qual você possa publicar, ou aguarde uma mensagem correspondente. O bot deve enviar o alerta ao `CHAT_ID` informado.

