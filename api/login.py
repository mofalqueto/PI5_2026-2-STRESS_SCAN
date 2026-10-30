
import os
from pathlib import Path
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, ConfigDict
from pwdlib import PasswordHash
from dotenv import load_dotenv

from database import db

load_dotenv(Path(__file__).resolve().parent / ".env")

SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY não configurada no .env")

ALGORITHM = "HS256"
TOKEN_EXPIRACAO_MINUTOS = 60

router = APIRouter()
password_hash = PasswordHash.recommended()


# Dados recebidos no login
class UsuarioLogin(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    senha: str


# Rota de autenticação
@router.post("/login")
def fazer_login(dados: UsuarioLogin):

    email = str(dados.email).strip().lower()

    # Procurar usuário no MongoDB
    usuario = db.usuarios.find_one({"email": email})

    # Verificar e-mail e senha
    if (
        not usuario
        or not password_hash.verify(
            dados.senha,
            usuario["senha_hash"]
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Definir prazo de validade do token
    agora = datetime.now(timezone.utc)
    expiracao = agora + timedelta(
        minutes=TOKEN_EXPIRACAO_MINUTOS
    )

    # Criar token JWT
    dados_token = {
        "sub": str(usuario["_id"]),
        "iat": agora,
        "exp": expiracao,
        "type": "access"
    }

    token = jwt.encode(
        dados_token,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": TOKEN_EXPIRACAO_MINUTOS * 60
    }
