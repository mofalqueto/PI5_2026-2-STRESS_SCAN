
import jwt

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from database import db
from login import SECRET_KEY, ALGORITHM

router = APIRouter()

# Autenticação por token Bearer
seguranca = HTTPBearer(auto_error=False)


def obter_usuario_atual(
    credenciais: HTTPAuthorizationCredentials = Depends(seguranca)
):
    # Verificar se o token foi enviado
    if credenciais is None:
        raise HTTPException(
            status_code=401,
            detail="Autenticação necessária."
        )

    try:
        # Validar assinatura e expiração do token
        dados_token = jwt.decode(
            credenciais.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        usuario_id = dados_token.get("sub")
        tipo_token = dados_token.get("type")

        if not usuario_id or tipo_token != "access":
            raise ValueError("Token inválido")

        # Procurar o usuário no MongoDB
        usuario = db.usuarios.find_one({
            "_id": ObjectId(usuario_id)
        })

        if usuario is None:
            raise ValueError("Usuário não encontrado")

        return usuario

    except (jwt.InvalidTokenError, ValueError, InvalidId):
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"}
        )


# Rota protegida para testar a autenticação
@router.get("/me")
def meu_perfil(usuario=Depends(obter_usuario_atual)):
    return {
        "usuario_id": str(usuario["_id"]),
        "email": usuario["email"],
        "mensagem": "Usuário autenticado com sucesso!"
    }
