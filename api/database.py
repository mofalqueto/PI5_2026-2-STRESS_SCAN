
import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient

# Carregar as configurações do arquivo .env
load_dotenv(Path(__file__).resolve().parent / ".env")

# Configurações do MongoDB Atlas
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")

if not MONGODB_URI or not MONGODB_DATABASE:
    raise ValueError("Configurações do MongoDB não encontradas no .env")

# Criar conexão com o MongoDB
client = MongoClient(
    MONGODB_URI,
    serverSelectionTimeoutMS=8000
)

# Selecionar o banco de dados
db = client[MONGODB_DATABASE]

# Testar a conexão
if __name__ == "__main__":
    try:
        client.admin.command("ping")
        print("Conexão com MongoDB Atlas realizada com sucesso!")
        print("Banco de dados configurado:", MONGODB_DATABASE)

    except Exception as erro:
        print("Erro de conexão:", type(erro).__name__)
        print("Verifique a string de conexão e as permissões de acesso.")
