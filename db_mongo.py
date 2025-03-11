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


def sintetiza_bruto():

    agora = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    filtro = {
        "objetoCompra": { 
            "$regex": "(software)", 
            "$options": "i"
        },
        "dataEncerramentoProposta": { 
            "$gt": agora
        }
    }
    
    chaves_selecionadas = {
        "objetoCompra": 1,
        "dataEncerramentoProposta": 1,
        "valorTotalEstimado": 1
        # "_id": 0  # Oculta o campo "_id"
    }
    

    total_registros = pncp_bruto.count_documents(filtro)
    # print('\n')
    # print(total_registros)
    # print('\n')



    consulta = pncp_bruto.find(filtro)
    list_registros = []
    for documento in consulta:

        # documento['valorTotalEstimado']         = locale.currency(documento['valorTotalEstimado'], grouping=True, symbol="R$ ")
        # documento['dataEncerramentoProposta']   = str(documento['dataEncerramentoProposta']).replace('T',' ')

        # valor_formatado = locale.currency(documento['valorTotalEstimado'], grouping=True, symbol="R$ ")        
        # datahora_formatada = str(documento['dataEncerramentoProposta']).replace('T',' ')

        # print('\n')
        # print(f'valorTotalEstimado       - '+valor_formatado                             ) 
        # print(f'dataEncerramentoProposta - '+datahora_formatada                          ) 
        # print(f'_id                      - '+str(documento['_id'                       ])) 
        # print(f'objetoCompra             - '+str(documento['objetoCompra'              ])) 
        # print('\n')    
        
        ano_CtPNCP = str(documento['numeroControlePNCP']).split('/')[-1]
        cli_CtPNCP = str(documento['numeroControlePNCP']).split('-')[0]
        num_CtPNCP = int(str(documento['numeroControlePNCP']).split('-')[-1].split('/')[0])
        link = f'https://pncp.gov.br/app/editais/{cli_CtPNCP}/{ano_CtPNCP}/{num_CtPNCP}'
        
        list_registros.append({
            'valorTotalEstimado': locale.currency(documento['valorTotalEstimado'], grouping=True, symbol="R$ ")
            ,'dataEncerramentoProposta':str(documento['dataEncerramentoProposta']).replace('T',' ')
            ,'objetoCompra':documento['objetoCompra']
            ,'link':link
        })

    # return {"total_registros":total_registros,"list_registros":list_registros}
    return list_registros



if __name__ == "__main__":
    consulta = sintetiza_bruto()
    print(consulta)
    for registro in consulta:
        print('\n')
        print(registro)
        print('\n')


    pass