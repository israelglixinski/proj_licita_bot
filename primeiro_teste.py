import os
from pymongo import MongoClient

mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017/meubanco")
client = MongoClient(mongo_url)
db = client["meubanco"]

# Exemplo de inserção
db.coleta.insert_one({"mensagem": "Olá do robô!"})

print("Documento inserido com sucesso!")

consulta = db.coleta.find()

for documento in consulta:
    print(documento)




