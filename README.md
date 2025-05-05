# Atlas — InsideBot

Atlas é o assistente interno de conhecimento da Inside Tecnologia, integrando Discord, OpenAI e Google Cloud para gerenciar, transcrever e organizar reuniões e informações de projetos.

---

## Funcionalidades

- Entrar em canais de voz e transcrever conversas automaticamente *(temporariamente desativado)*
- Gerar atas de reunião e salvá-las no Google Drive (formato Google Docs) *(temporariamente desativado)*
- Atualizar uma base de conhecimento vetorizada para consultas futuras *(temporariamente desativado)*
- Registrar reuniões em uma planilha Google Sheets *(temporariamente desativado)*
- Responder perguntas baseadas no conhecimento interno da empresa *(temporariamente desativado)*
- Receber perguntas via chat e responder com base em contexto interno

---

## Comandos Principais

| Comando         | Descrição                                                            |
|----------------|----------------------------------------------------------------------|
| `/joinvoice`   | Entra no canal de voz e começa a transcrever *(desabilitado)*        |
| `/leavevoice`  | Sai do canal de voz, gera resumo e ata *(desabilitado)*              |
| Menção @Atlas  | Responde a perguntas relacionadas ao conhecimento interno            |

---

## Estrutura do Projeto

```bash
atlas/
├── bot.py                    # Lógica principal do bot
├── utils/
│   ├── openai_utils.py       # Integração com o Assistente da OpenAI
│   ├── vector_utils.py       # Busca vetorial com LangChain e ChromaDB
├── .env                      # Variáveis de ambiente (DISCORD_TOKEN, OPENAI_API_KEY, etc.)
├── requirements.txt          # Dependências
└── logs/errors.log           # Registro de erros
