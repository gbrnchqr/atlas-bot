import openai
import os
import time
from dotenv import load_dotenv
from utils.vector_utils import search_knowledge_base

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MAX_TOKENS = 1000
MAX_WAIT_SECONDS = 15

async def ask_openai_assistant(question):
    assistant_id = os.getenv("OPENAI_ASSISTANT_ID")

    if not assistant_id:
        return "❌ O ID do assistente não está definido. Verifique o arquivo .env."

    if len(question) > MAX_TOKENS:
        return "⚠️ Sua pergunta é muito longa. Por favor, resuma para menos de 1000 caracteres."

    contexto = search_knowledge_base(question)
    thread = client.beta.threads.create()

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"Contexto:\n{contexto}\n\nPergunta:\n{question}\n\nObservação: não é necessário citar fontes. Apenas responda de forma objetiva."
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    start_time = time.time()
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run_status.status == "completed":
            break
        if time.time() - start_time > MAX_WAIT_SECONDS:
            return "⏳ A resposta demorou demais. Tente novamente mais tarde."
        time.sleep(1)

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    try:
        for msg in messages.data:
            dumped = msg.model_dump()
            for content in dumped.get("content", []):
                if isinstance(content, dict) and content.get("type") == "text":
                    return content["text"].get("value", "")

    except Exception as e:
        print(f"[DEBUG] Erro ao interpretar resposta do assistente: {e}")

    return "❌ Não foi possível obter uma resposta do assistente."

def create_summary_with_context(audio_path):
    return "Resumo desabilitado: funcionalidades de áudio foram removidas."
