import discord
import os
import logging
import traceback
import re
from discord.ext import commands
from dotenv import load_dotenv
from utils.openai_utils import ask_openai_assistant

print("[DEBUG] Iniciando o Atlas Bot...")

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

if not DISCORD_TOKEN:
    print("❌ DISCORD_TOKEN não encontrado no .env")
    exit(1)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

os.makedirs("logs", exist_ok=True)

logging.basicConfig(filename='logs/errors.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Corrige citações de fontes no estilo "4:0†source】" para markdown do Discord

def ajustar_links_discord(resposta):
    # Substitui citações no estilo "4:0†source】" por [source](link_ficticio)
    resposta = re.sub(r"\d+:\d+†source【?source?】?|【?source?】?", "[source](https://example.com)", resposta)
    # Substitui "Fonte: http://..." por [source](...)
    resposta = re.sub(r"(Fonte[s]?:\s*)(https?://\S+)", r"\1[source](\2)", resposta)
    return resposta

@bot.event
async def on_ready():
    print(f"Bot Atlas conectado como {bot.user}")

@bot.event
async def on_message(message):
    try:
        if message.author == bot.user:
            return

        # Se for canal, só responde se for mencionado diretamente
        if message.guild and bot.user.mentioned_in(message) is False:
            return

        if len(message.content) > 1000:
            await message.channel.send("⚠️ A mensagem é muito longa. Por favor, resuma sua pergunta.")
            return

        resposta = await ask_openai_assistant(message.content)
        resposta_formatada = ajustar_links_discord(resposta)
        await message.channel.send(resposta_formatada)

    except Exception as e:
        logging.error("Erro ao responder mensagem:", exc_info=True)
        print("[DEBUG] Erro interno:")
        traceback.print_exc()
        await message.channel.send("❌ Erro ao processar sua mensagem.")

print("[DEBUG] Executando bot.run()")
bot.run(DISCORD_TOKEN)
