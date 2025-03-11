import font_api
from datetime import datetime, timedelta
import db_mongo

def analise_dia_a_dia():
    api = font_api.Pncp()
    api.pagina = 1
    api.codigoModalidadeContratacao = 1

    loop_dataInicial = "20250221"
    loop_dataFinal = "20250226"
    loop_atual = loop_dataInicial
    loop_status = True
    loop_last_lap = False

    print("\n")
    while loop_status:
        if loop_last_lap:
            loop_status = False

        api.dataInicial = loop_atual
        api.dataFinal = loop_atual
        consulta = api.consulta_contratacoes_puplicacao()

        try:
            print(f"{api.dataInicial} - {len(consulta['data'])}")
        except:
            print(f"{api.dataInicial} - {consulta}")

        loop_atual = (
            datetime.strptime(loop_atual, "%Y%m%d") + timedelta(days=1)
        ).strftime("%Y%m%d")
        if loop_atual == loop_dataFinal:
            loop_last_lap = True
        pass

    pass


def analise_entre_datas(codigoModalidadeContratacao):
    api = font_api.Pncp()
    api.pagina = 1
    api.codigoModalidadeContratacao = codigoModalidadeContratacao
    api.tamanhoPagina = 10
    api.dataInicial = "20250101"
    api.dataFinal = "20250226"

    print("\n")
    consulta = api.consulta_contratacoes_puplicacao()

    # try:
    #     print(f'{api.dataInicial} - {len(consulta['data'])}')
    # except:
    #     print(f'{api.dataInicial} - {consulta}')

    primeiro = True
    for registro in consulta["data"]:

        if primeiro:
            print(f"{registro['modalidadeId']}---{registro['modalidadeNome']}---")
        primeiro = False
    pass


def alimentador_mongo():
    lista_ModalidadeContratacao = [
        # [1, "Leilão - Eletrônico"],
        # [2, "Diálogo Competitivo"],
        # [3, "Concurso"],
        # [4, "Concorrência - Eletrônica"],
        # [5, "Concorrência - Presencial"],
        [6, "Pregão - Eletrônico"]
        # [7, "Pregão - Presencial"],
        # [8, "Dispensa"],
        # [9, "Inexigibilidade"],
        # [10, "Manifestação de Interesse"],
        # [11, "Pré-qualificação"],
        # [12, "Credenciamento"],
        # [13, "Leilão - Presencial"],
        # [14, "Inaplicabilidade da Licitação"],
    ]

    api = font_api.Pncp()

    for modalidade in lista_ModalidadeContratacao:
        api.codigoModalidadeContratacao = modalidade[0]
        api.pagina          = 1
        api.tamanhoPagina   = 50
        api.dataInicial     = "20250101"
        api.dataFinal       = "20251231"


        consulta_inicial = api.consulta_contratacoes_puplicacao()
     
        try:
            totalRegistros   = consulta_inicial["totalRegistros"  ]                
            totalPaginas     = consulta_inicial["totalPaginas"    ]                
            numeroPagina     = consulta_inicial["numeroPagina"    ]                
            paginasRestantes = consulta_inicial["paginasRestantes"]                    
        except:
            totalRegistros   = 0
            totalPaginas     = 0
            numeroPagina     = 0
            paginasRestantes = 0

        print(' \n ')
        print(f'modalidade       - {modalidade        }')
        print(f'totalRegistros   - {totalRegistros    }')
        print(f'totalPaginas     - {totalPaginas      }')

        if totalRegistros > 0:
            pagina_atual = 1
            while pagina_atual <= totalPaginas:
                api.pagina = pagina_atual
                consulta_in_loop = api.consulta_contratacoes_puplicacao()

                for registro in consulta_in_loop['data']:

                    # print(registro)
                    # db_mongo.colecao.insert_one(registro)

                    pass

                pagina_atual +=1
                pass
            
            pass


        pass



if __name__ == "__main__":
    # analise_dia_a_dia()
    # atual = 0
    # while True:
    #     atual += 1
    #     analise_entre_datas(atual)
    # alimentador_mongo()

    pass
