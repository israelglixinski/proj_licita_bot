from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import locale
import os


# Conexão com o Mongo
load_dotenv()
mongopass = os.getenv("mongopass")
client = MongoClient(f"mongodb+srv://israelglixinski:{mongopass}@cluster0.kzkzrs2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["licitacao"]
pncp_bruto = db["pncp_bruto"]
pncp_final = db["pncp_final"]

# Configurar locale para formato monetário brasileiro
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')



if __name__ == "__main__":
   pass