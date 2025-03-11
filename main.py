from datetime import datetime
import font_api
import db_mongo



def alimentador_bruto_mongo():
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
                agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # print('\n\n')
                print(f"{agora} - Página {pagina_atual} de {totalPaginas} ")
                for registro in consulta_in_loop['data']:
                    # print(".", end="")
                    # print(registro)
                    db_mongo.pncp_bruto.insert_one(registro)
                    pass

                pagina_atual +=1
                pass
            pass
        pass

def alimentador_final_mongo():
    pass



if __name__ == '__main__':
    alimentador_bruto_mongo()
    pass