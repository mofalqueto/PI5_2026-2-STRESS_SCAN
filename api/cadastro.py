
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from pwdlib import PasswordHash
from pymongo.errors import DuplicateKeyError

from database import db

router = APIRouter()
password_hash = PasswordHash.recommended()


class UsuarioCadastro(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    senha: str = Field(min_length=8, max_length=128)


@router.post("/cadastro", status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(dados: UsuarioCadastro):

    email = str(dados.email).strip().lower()

    senha_hash = password_hash.hash(dados.senha)

    novo_usuario = {
        "email": email,
        "senha_hash": senha_hash,
        "criado_em": datetime.now(timezone.utc)
    }

    try:
        resultado = db.usuarios.insert_one(novo_usuario)

    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail="E-mail já cadastrado."
        )

    return {
        "mensagem": "Usuário cadastrado com sucesso!",
        "usuario_id": str(resultado.inserted_id),
        "email": email
    }
