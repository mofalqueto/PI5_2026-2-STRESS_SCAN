
from database import db
from pymongo import ASCENDING, DESCENDING

# Coleção de usuários
# Impede o cadastro de dois usuários com o mesmo e-mail
db.usuarios.create_index(
    [("email", ASCENDING)],
    unique=True,
    name="email_unico"
)

# Coleção de avaliações
# Facilita consultar o histórico de cada estudante por data
db.avaliacoes.create_index(
    [
        ("usuario_id", ASCENDING),
        ("criado_em", DESCENDING)
    ],
    name="historico_por_usuario"
)

print("Coleções e índices criados com sucesso!")
print("Banco de dados: stress_scan")
print("Coleções:", db.list_collection_names())
