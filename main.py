from datetime import datetime
import font_api  # Importa o módulo que interage com a API de fontes de dados
import db_mongo  # Importa o módulo para interação com o MongoDB


def alimentador_bruto_mongo():
    # # Lista contendo modalidades de contratação (somente "Pregão - Eletrônico" está ativado)
    # lista_ModalidadeContratacao = [
    #     # [1, "Leilão - Eletrônico"],
    #     # [2, "Diálogo Competitivo"],
    #     # [3, "Concurso"],
    #     [4, "Concorrência - Eletrônica"],
    #     [5, "Concorrência - Presencial"],
    #     [6, "Pregão - Eletrônico"],
    #     [7, "Pregão - Presencial"],
    #     [8, "Dispensa"],
    #     [9, "Inexigibilidade"],
    #     # [10, "Manifestação de Interesse"],
    #     # [11, "Pré-qualificação"],
    #     [12, "Credenciamento"]
    #     # [13, "Leilão - Presencial"],
    #     # [14, "Inaplicabilidade da Licitação"],
    # ]
    # Lista contendo modalidades de contratação (somente "Pregão - Eletrônico" está ativado)
    lista_ModalidadeContratacao = [
        # [1, "Leilão - Eletrônico"],
        # [2, "Diálogo Competitivo"],
        # [3, "Concurso"],
        # [4, "Concorrência - Eletrônica"],
        # [5, "Concorrência - Presencial"],
        [6, "Pregão - Eletrônico"],
        # [7, "Pregão - Presencial"],
        # [8, "Dispensa"],
        # [9, "Inexigibilidade"],
        # [10, "Manifestação de Interesse"],
        # [11, "Pré-qualificação"],
        # [12, "Credenciamento"]
        # [13, "Leilão - Presencial"],
        # [14, "Inaplicabilidade da Licitação"],
    ]

    api = font_api.Pncp()

    # Itera sobre cada modalidade de contratação na lista
    for modalidade in lista_ModalidadeContratacao:
        api.codigoModalidadeContratacao = modalidade[0]  # Define o código da modalidade
        api.pagina = 1  # Define a página inicial da API
        api.tamanhoPagina = 50  # Define o número de registros por página
        # api.dataInicial = "20250101"  # Define a data inicial para consulta
        # api.dataFinal = "20251231"  # Define a data final para consulta
        api.dataInicial = "20250301"  # Define a data inicial para consulta
        api.dataFinal = "20250315"  # Define a data final para consulta

        # Realiza a consulta inicial na API
        consulta_inicial = api.consulta_contratacoes_puplicacao()
     
        # Trata possíveis exceções ao tentar acessar os dados da API
        try:
            totalRegistros = consulta_inicial["totalRegistros"]  # Total de registros retornados
            totalPaginas = consulta_inicial["totalPaginas"]  # Total de páginas na consulta
            numeroPagina = consulta_inicial["numeroPagina"]  # Número da página atual
            paginasRestantes = consulta_inicial["paginasRestantes"]  # Páginas restantes
        except:
            # Caso ocorra um erro, define valores padrão como zero
            totalRegistros = 0
            totalPaginas = 0
            numeroPagina = 0
            paginasRestantes = 0

        # Exibe no console informações sobre a consulta inicial
        print(' \n ')
        print(f'modalidade       - {modalidade}')
        print(f'totalRegistros   - {totalRegistros}')
        print(f'totalPaginas     - {totalPaginas}')

        # Caso existam registros a serem processados
        if totalRegistros > 0:
            pagina_atual = 1
            # Itera sobre todas as páginas disponíveis
            while pagina_atual <= totalPaginas:
                api.pagina = pagina_atual  # Define a página atual na API
                consulta_in_loop = api.consulta_contratacoes_puplicacao()  # Realiza nova consulta
                agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Obtém o timestamp atual
                # print('\n\n')
                print(f"{agora} - Página {pagina_atual} de {totalPaginas} ")  # Exibe progresso
                
                # Itera sobre os registros da página atual
                for registro in consulta_in_loop['data']:
                    # print(".", end="")
                    # print(registro)
                    db_mongo.pncp_bruto.insert_one(registro)
                    pass

                pagina_atual += 1  # Incrementa o contador da página
                pass
            pass
        pass

def alimentador_final_mongo():
    # Obtém os registros processados do banco MongoDB
    consulta = db_mongo.sintetiza_bruto()
    
    # Itera sobre os registros retornados
    for registro in consulta:
        registro['interesse'] = 'Não Avaliado'  # Adiciona um campo de interesse
        registro['anotacao'] = 'whatsapp'  # Adiciona um campo de anotações
        
        db_mongo.pncp_final.insert_one(registro)  # Insere os registros no banco final
    pass


if __name__ == '__main__':
    # Executa apenas a função alimentador_final_mongo(), a outra está comentada
    alimentador_bruto_mongo()
    # alimentador_final_mongo()
    pass
