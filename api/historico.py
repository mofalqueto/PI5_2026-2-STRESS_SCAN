
from datetime import timezone

from fastapi import APIRouter, Depends
from pymongo import DESCENDING

from database import db
from auth import obter_usuario_atual

router = APIRouter()


@router.get("/historico")
def consultar_historico(
    usuario=Depends(obter_usuario_atual)
):

    # Identificar o estudante autenticado
    usuario_id = str(usuario["_id"])

    # Buscar somente as avaliações desse estudante
    avaliacoes = db.avaliacoes.find(
        {"usuario_id": usuario_id}
    ).sort(
        "criado_em", DESCENDING
    ).limit(50)

    # Organizar os resultados
    historico = []

    for avaliacao in avaliacoes:
        data = avaliacao["criado_em"]

        if data.tzinfo is None:
            data = data.replace(tzinfo=timezone.utc)

        historico.append({
            "avaliacao_id": str(avaliacao["_id"]),
            "nivel_estresse": avaliacao["nivel_estresse"],
            "classificacao": avaliacao["classificacao"],
            "criado_em": data.isoformat()
        })

    return {
        "usuario_id": usuario_id,
        "total_retornado": len(historico),
        "avaliacoes": historico
    }
