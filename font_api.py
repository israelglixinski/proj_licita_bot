import requests
from datetime import datetime

class Pncp:
    # Definição das URLs base da API
    BASE_URL_V0 = "https://pncp.gov.br/api"
    BASE_URL_V1 = "https://pncp.gov.br/api/consulta/v1"
    
    # Exemplo de endpoint de busca
    'https://pncp.gov.br/api/search/?q=software&tipos_documento=edital&ordenacao=-data&pagina=1&tam_pagina=500&status=recebendo_proposta&modalidades=6%7C7%7C10'

    def __init__(self,
                 dataInicial                    : str = datetime.now().strftime('%Y%m%d'),
                 dataFinal                      : str = datetime.now().strftime('%Y%m%d'),
                 pagina                         : int = 1,
                 codigoModalidadeContratacao    : int = 1,
                 tamanhoPagina                  : int = 50):
        """
        Inicializa a classe com os parâmetros para consulta na API.
        
        :param dataInicial: Data inicial da consulta (formato YYYYMMDD).
        :param dataFinal: Data final da consulta (formato YYYYMMDD).
        :param pagina: Número da página de consulta.
        :param codigoModalidadeContratacao: Código da modalidade de contratação.
        :param tamanhoPagina: Quantidade de registros por página.
        """
        self.dataInicial                    = dataInicial
        self.dataFinal                      = dataFinal
        self.pagina                         = pagina
        self.codigoModalidadeContratacao    = codigoModalidadeContratacao
        self.tamanhoPagina                  = tamanhoPagina

    def consulta_contrato(self):
        """
        Consulta os contratos na API.
        
        :return: Resposta da API em formato JSON ou erro caso a requisição falhe.
        """
        metodo = '/contratos'
        full_endpoint = self.BASE_URL_V1 + metodo
        params = {
            "dataInicial"   : self.dataInicial,
            "dataFinal"     : self.dataFinal,
            "pagina"        : self.pagina
        }
        headers = {"accept": "*/*"}
        
        response = requests.get(full_endpoint, params=params, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Erro {response.status_code}: {response.text}"}

    def consulta_contratacoes_puplicacao(self):
        """
        Consulta as publicações de contratações na API.
        
        :return: Resposta da API em formato JSON ou erro caso a requisição falhe.
        """
        metodo = '/contratacoes/publicacao'
        full_endpoint = self.BASE_URL_V1 + metodo
        params = {
            "dataInicial"                   : self.dataInicial,
            "dataFinal"                     : self.dataFinal,
            "pagina"                        : self.pagina,
            "codigoModalidadeContratacao"   : self.codigoModalidadeContratacao,
            "tamanhoPagina"                 : self.tamanhoPagina
        }
        headers = {"accept": "*/*"}
        
        response = requests.get(full_endpoint, params=params, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Erro {response.status_code}: {response.text}"}

    def consulta_editais_site(self):
        """
        Consulta editais diretamente pelo site da API.
        
        :return: Resposta da API em formato JSON ou erro caso a requisição falhe.
        """
        metodo = '/search/?q=software&tipos_documento=edital&ordenacao=-data&pagina=1&tam_pagina=500&status=recebendo_proposta&modalidades=6%7C7%7C10'
        full_endpoint = self.BASE_URL_V0 + metodo
        params = {
            "dataInicial"                   : self.dataInicial,
            "dataFinal"                     : self.dataFinal,
            "pagina"                        : self.pagina,
            "codigoModalidadeContratacao"   : self.codigoModalidadeContratacao,
            "tamanhoPagina"                 : self.tamanhoPagina
        }
        headers = {"accept": "*/*"}
        
        response = requests.get(full_endpoint, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Erro {response.status_code}: {response.text}"}

# Exemplo de uso
if __name__ == "__main__":
    # Define os parâmetros da consulta
    data_inicial    = "20250101"
    data_final      = "20250101"
    pagina          = 1
    
    # Instancia a classe com os parâmetros definidos
    api = Pncp(data_inicial, data_final, pagina)
    # resultado = api.consulta_contrato()
    # print(resultado)
    consulta = api.consulta_editais_site() 

    for item in consulta['items']:
        print('\n')
        print(item)
        print('\n')
