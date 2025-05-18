from datetime import datetime
import font_api  # Importa o módulo que interage com a API de fontes de dados
import db_mongo_local  # Importa o módulo para interação com o MongoDB
import db_mongo_nuvem  # Importa o módulo para interação com o MongoDB


def registrando(texto):
    arquivo = open('log.txt','a')
    agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mensagem = f"""{agora} - {texto}"""
    print(mensagem,file=arquivo)
    print(mensagem)
    arquivo.close()
    pass


def alimentador_bruto_mongo():
    # Lista contendo modalidades de contratação (somente "Pregão - Eletrônico" está ativado)
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
        [4, "Concorrência - Eletrônica"],
        [5, "Concorrência - Presencial"],
        [6, "Pregão - Eletrônico"],
        [7, "Pregão - Presencial"],
        [8, "Dispensa"],
        [9, "Inexigibilidade"],
        [12, "Credenciamento"]
    ]
    
    
  

    api = font_api.Pncp()




    list_datas = [
         "20250501"
        ,"20250502"
        ,"20250503"
        ,"20250504"
        ,"20250505"
        ,"20250506"
        ,"20250507"
        ,"20250508"
        ,"20250509"
        ,"20250510"
        ,"20250511"
        ,"20250512"
        ,"20250513"
        ,"20250514"
        ,"20250515"
        ,"20250516"
        ,"20250517"
        ,"20250518"
        ,"20250519"
        ,"20250520"
        ]


    for modalidade in lista_ModalidadeContratacao:
        registrando(f'trabalhando na modalidade {modalidade}')

        # Itera sobre cada modalidade de contratação na lista
        for data_process in list_datas:
            registrando(f'trabalhando na data {data_process}')
            api.codigoModalidadeContratacao = modalidade[0]  # Define o código da modalidade
            desc_modalidade = modalidade[1]  # Define o código da modalidade
            api.pagina = 1  # Define a página inicial da API
            api.tamanhoPagina = 50  # Define o número de registros por página
            # api.dataInicial = "20250101"  # Define a data inicial para consulta
            # api.dataFinal = "20251231"  # Define a data final para consulta
            api.dataInicial = data_process  # Define a data inicial para consulta
            api.dataFinal   = data_process  # Define a data final para consulta

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
            # registrando(' \n ')
            # registrando(f'modalidade       - {modalidade}')
            # registrando(f'totalRegistros   - {totalRegistros}')
            # registrando(f'totalPaginas     - {totalPaginas}')

            registrando(f'PONTO DE MARCACAO / modalidade - {modalidade} / Data - {data_process} / totalPaginas - {totalPaginas} / totalRegistros - {totalRegistros}')




            # Caso existam registros a serem processados
            if totalRegistros > 0:
                pagina_atual = 1
                # Itera sobre todas as páginas disponíveis
                while pagina_atual <= totalPaginas:
                    tentativa = True
                    while tentativa:
                        try:
                            api.pagina = pagina_atual  # Define a página atual na API
                            consulta_in_loop = api.consulta_contratacoes_puplicacao()  # Realiza nova consulta
                            agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Obtém o timestamp atual
                            # print('\n\n')
                            registrando(f"{agora} - Página {pagina_atual} de {totalPaginas} ")  # Exibe progresso
                            
                            # Itera sobre os registros da página atual
                            for registro in consulta_in_loop['data']:
                                numero_controle = registro.get("numeroControlePNCP")
                                if not numero_controle:
                                    registrando("Registro sem numeroControlePNCP, ignorado.")
                                    continue

                                existe = db_mongo_local.pncp_bruto.find_one({"numeroControlePNCP": numero_controle})
                                
                                if existe:
                                    registrando(f"{desc_modalidade}-{data_process}-{totalRegistros}-{pagina_atual}/{totalPaginas} - Já existe no banco: {numero_controle}")
                                else:
                                    db_mongo_local.pncp_bruto.insert_one(registro)
                                    registrando(f"{desc_modalidade}-{data_process}-{totalRegistros}-{pagina_atual}/{totalPaginas} - Inserido novo registro: {numero_controle}")
                            tentativa = False
                            
                        except:
                            tentativa = True
                        registrando(f"Tentativa = {tentativa}")

                    pagina_atual += 1  # Incrementa o contador da página
                    pass
                pass
            pass




def alimentador_final_mongo():
    # Obtém os registros processados do banco MongoDB

    agora = datetime.now().strftime("%Y-%m-%d")

    lista_termos = [    
    'telemarketing'
    ,'teleatendimento'
    ,'telefonia'
    ,'webchat'
    ,'chatbot'
    ,'telefônico'
    ,'0800'
    ,'whatsapp'
    ,'software'    
    ,'python'    
    ]
    
    for termo in lista_termos:

        consulta = db_mongo_local.sintetiza_bruto(termo)

        registrando(f"FINAL - {termo} - {len(consulta)}")

        # Itera sobre os registros retornados
        for registro in consulta:
            registro['interesse'] = 'Não Avaliado'  # Adiciona um campo de interesse
            registro['anotacao'] = f"{termo} {agora}"  # Adiciona um campo de anotações
            

            existe = db_mongo_nuvem.pncp_final.find_one({"link": registro["link"]})
            
            if existe:
                registrando(f"ALIMENTA_FINAL-{termo}-{registro["dataEncerramentoProposta"]}-Já existe no banco: {registro["link"]}")
            else:
                db_mongo_nuvem.pncp_final.insert_one(registro)  # Insere os registros no banco final
                registrando(f"ALIMENTA_FINAL-{termo}-{registro["dataEncerramentoProposta"]}-Inserido novo registro: {registro["link"]}")




        pass


if __name__ == '__main__':
    # Executa apenas a função alimentador_final_mongo(), a outra está comentada
    alimentador_bruto_mongo()
    # alimentador_final_mongo()
    pass
