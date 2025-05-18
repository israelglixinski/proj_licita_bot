from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import locale
import os

# Carrega variáveis de ambiente do arquivo .env
# load_dotenv()

# Obtém a senha do MongoDB a partir das variáveis de ambiente
# mongopass = os.getenv("MONGO_PASS")

# Configura a conexão com o MongoDB usando a senha carregada
# client = MongoClient(f"mongodb+srv://israelglixinski:{mongopass}@cluster0.kzkzrs2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017/meubanco")
client = MongoClient(mongo_url)


# Seleciona o banco de dados "licitacao"
db = client["licitacao"]

# Define as coleções a serem utilizadas
pncp_bruto = db["pncp_bruto"]
pncp_final = db["pncp_final"]

# Configura o locale para o formato monetário brasileiro
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def sintetiza_bruto(termo):
    """
    Filtra e formata os registros da coleção pncp_bruto para exibição.
    
    :return: Lista de registros formatados com valores monetários e links.
    """
    
    # Obtém a data e hora atuais no formato adequado para comparação
    agora = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    
    # Define o filtro para buscar apenas registros que contenham "software" no objeto de compra
    # e cuja data de encerramento da proposta seja futura.
    # filtro = {
    #     "objetoCompra": { 
    #         "$regex": "(software)",  # Busca pelo termo "software" (case insensitive)
    #         "$options": "i"
    #     },
    #     "dataEncerramentoProposta": { 
    #         "$gt": agora  # Apenas propostas que ainda não encerraram
    #     }
    # }
    
    
    #telemarketing
    #teleatendimento
    #telefonia
    #webchat
    #chatbot
    #telefônico
    #0800
    #whatsapp
    #
    #
    #
    
    
    filtro = {
        "objetoCompra": { 
            "$regex": f"({termo})",  # Busca pelo termo (case insensitive)
            "$options": "i"
        },
        "dataEncerramentoProposta": { 
            "$gt": agora  # Apenas propostas que ainda não encerraram
        }
    }
    
    # Define os campos que serão retornados na consulta
    chaves_selecionadas = {
        "objetoCompra": 1,
        "dataEncerramentoProposta": 1,
        "valorTotalEstimado": 1
        # "_id": 0  # Se quiser ocultar o campo "_id", basta descomentar esta linha
    }
    
    # Conta o total de registros que atendem ao filtro
    total_registros = pncp_bruto.count_documents(filtro)
    # print('\n')
    # print(total_registros)
    # print('\n')



    consulta = pncp_bruto.find(filtro)
    # consulta = pncp_bruto.find()
    
    # Lista onde serão armazenados os registros formatados
    list_registros = []
    
    # Processa os documentos retornados na consulta
    for documento in consulta:

        # print(documento)

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
        
        # Adiciona o registro formatado à lista de resultados
        list_registros.append({
            'valorTotalEstimado': locale.currency(documento['valorTotalEstimado'], grouping=True, symbol="R$ ")
            ,'dataEncerramentoProposta':str(documento['dataEncerramentoProposta']).replace('T',' ')
            ,'objetoCompra':documento['objetoCompra']
            ,'link':link
        })

    # return {"total_registros":total_registros,"list_registros":list_registros}
    return list_registros

if __name__ == "__main__":
    # Chama a função de consulta e exibe os resultados
    # consulta = sintetiza_bruto()
    # for registro in consulta:
    #     print('\n')
    #     print(registro)
    #     print('\n')
    # print(len(consulta))


    # consulta = pncp_bruto.find()
    # for registro in consulta: 
    #     print('\n')
    #     print(f"'dataAberturaProposta'      - {registro['dataAberturaProposta'      ]}")
    #     print(f"'dataEncerramentoProposta'  - {registro['dataEncerramentoProposta'  ]}")
    #     print(f"'dataInclusao'              - {registro['dataInclusao'              ]}")
    #     print(f"'dataPublicacaoPncp'        - {registro['dataPublicacaoPncp'        ]}")
    #     print(f"'dataAtualizacao'           - {registro['dataAtualizacao'           ]}")
    #     print(f"'dataAtualizacaoGlobal'     - {registro['dataAtualizacaoGlobal'     ]}")
    #     print('\n')


    consulta = pncp_bruto.find({"numeroControlePNCP":"31752645000104-1-000023/2025"})
    for registro in consulta:
        print(registro)

    # pncp_bruto.delete_many({})
    # pncp_bruto.delete_one({"numeroControlePNCP": "01610566000106-1-000014/2025"})
    pass