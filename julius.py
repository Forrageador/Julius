import os
import re
import unicodedata
import asyncio
import requests
from dotenv import load_dotenv
from telethon import TelegramClient, events

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not API_ID or not API_HASH:
    raise RuntimeError("Credenciais da API não encontradas.")

if not BOT_TOKEN or not CHAT_ID:
    raise RuntimeError("Credenciais do bot não encontradas.")

try:
    API_ID = int(API_ID)
except ValueError as erro:
    raise RuntimeError("API_ID deve ser um número.") from erro

ALVOS = [
    "notebook",
    "fone de ouvido",
    "playstation",
    "bug",
]

CANAIS = [
    "@gatunopromos",
    "@pobres",
    "@LaPromotion",
    "@promonocontext",
]


def normalizar(texto: str) -> str:
    texto = texto.lower()
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in texto if not unicodedata.combining(c))

PADROES_ALVOS = [
    (palavra, re.compile(r"\b" + re.escape(normalizar(palavra)) + r"\b"))
    for palavra in ALVOS
]

client = TelegramClient("sessao_filtro", API_ID, API_HASH)


def contem_palavra_chave(texto: str) -> str | None:
    if not texto:
        return None

    texto_normalizado = normalizar(texto)
    for palavra, padrao in PADROES_ALVOS:
        if padrao.search(texto_normalizado):
            return palavra
    return None


def _notificar_via_bot_sync(mensagem: str) -> None:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        resposta = requests.post(
            url,
            data={"chat_id": CHAT_ID, "text": mensagem},
            timeout=10,
        )
        resposta.raise_for_status()
    except requests.RequestException as erro:
        print(f"[ERRO] Falha ao notificar via bot: {erro}")


async def notificar_via_bot(mensagem: str) -> None:
    await asyncio.to_thread(_notificar_via_bot_sync, mensagem)


@client.on(events.NewMessage(chats=CANAIS))
async def handler(event):
    texto = event.raw_text or ""
    palavra_encontrada = contem_palavra_chave(texto)

    if palavra_encontrada:
        canal = await event.get_chat()
        nome_canal = getattr(canal, "title", "canal desconhecido")

        await notificar_via_bot(
            f"🔔 Promoção encontrada: '{palavra_encontrada}'\n"
            f"📢 Canal: {nome_canal}\n\n"
            f"{texto}"
        )
        print(f"[BOA!] '{palavra_encontrada}' em {nome_canal}")


print("Filtro de promoções rodando...")
with client:
    client.run_until_disconnected()