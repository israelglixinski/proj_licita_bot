import requests
from datetime import datetime


class Pncp:
    BASE_URL_V0 = "https://pncp.gov.br/api"
    BASE_URL_V1 = "https://pncp.gov.br/api/consulta/v1"
    
    'https://pncp.gov.br/api/search/?q=software&tipos_documento=edital&ordenacao=-data&pagina=1&tam_pagina=500&status=recebendo_proposta&modalidades=6%7C7%7C10'


    def __init__(self
        , dataInicial                   : str = datetime.now().strftime('%Y%m%d') 
        , dataFinal                     : str = datetime.now().strftime('%Y%m%d')
        , pagina                        : int = 1
        , codigoModalidadeContratacao   : int = 1
        , tamanhoPagina                 : int = 50
        ):
        
        self.dataInicial                    = dataInicial
        self.dataFinal                      = dataFinal
        self.pagina                         = pagina
        self.codigoModalidadeContratacao    = codigoModalidadeContratacao
        self.tamanhoPagina                  = tamanhoPagina

    def consulta_contrato(self):
        metodo          = '/contratos'
        full_endpoint   = self.BASE_URL_V1+metodo
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
        metodo          = '/contratacoes/publicacao'
        full_endpoint   = self.BASE_URL_V1+metodo
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
        metodo          = '/search/?q=software&tipos_documento=edital&ordenacao=-data&pagina=1&tam_pagina=500&status=recebendo_proposta&modalidades=6%7C7%7C10'
        full_endpoint   = self.BASE_URL_V0+metodo
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
    data_inicial = "20250101"
    data_final = "20250101"
    pagina = 1
    
    api = Pncp(data_inicial, data_final, pagina)
    # resultado = api.consulta_contrato()
    # print(resultado)
    consulta = api.consulta_editais_site() 

    for item in consulta['items']:
        print('\n')
        print(item)
        print('\n')
