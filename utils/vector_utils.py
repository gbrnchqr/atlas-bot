import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

load_dotenv()

embedding = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))


def get_vectordb():
    try:
        return Chroma(
            collection_name="atlas-knowledge",
            persist_directory="vector_db",
            embedding_function=embedding
        )
    except Exception as e:
        print("[DEBUG] Erro ao iniciar ChromaDB:")
        import traceback
        traceback.print_exc()
        return None


def search_knowledge_base(query):
    vectordb = get_vectordb()
    if vectordb is None:
        return "Base vetorial indisponível no momento."

    docs = vectordb.similarity_search(query, k=3)
    return "\n".join([doc.page_content for doc in docs])
