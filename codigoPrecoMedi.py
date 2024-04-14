import requests
from bs4 import BeautifulSoup
import re
import statistics
import matplotlib.pyplot as plt

quantidade_pagina_trazida = 60

def fazer_pesquisa(pesquisa,num_pag=0):
    pagina_inicial = num_pag * quantidade_pagina_trazida
    url = f"https://www.google.com.br/search?q={pesquisa}&sca_esv=576e4e7685de117a&hl=pt-BR&psb=1&tbs=vw:d&tbm=shop&ei=kTwSZuPPJafX1sQP4_WU-Ac&start={pagina_inicial}&sa=N&ved=0ahUKEwij3NOlvK-FAxWnq5UCHeM6BX84PBDy0wMIsRU&biw=1318&bih=646&dpr=1"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        return BeautifulSoup(response.content, "html.parser")
    except:
        return "erro ao acessar o site."
    
def analise_Estatistica(dadosProduts):
    try:
        dic_prod = {}
        lista_valores_produtos = []
        [lista_valores_produtos.append(valores["valorProduto"]) for valores in dadosProduts] 
        if dadosProduts:
            dic_prod["media"] = statistics.mean(lista_valores_produtos)
            dic_prod["desvio_padrao"] = statistics.stdev(lista_valores_produtos)
            dic_prod["variancia"] = statistics.variance(lista_valores_produtos)
            dic_prod["mediana"] = statistics.median(lista_valores_produtos)
            dic_prod["moda"] = statistics.mode(lista_valores_produtos)
            dic_prod["media_geometrica"] = statistics.geometric_mean(lista_valores_produtos)
            dic_prod["media_harmonica"] = statistics.harmonic_mean(lista_valores_produtos) 
            dic_prod["menor_valor_encontrado"] = min(lista_valores_produtos) 
            dic_prod["maior_valor_encontrado"] = max(lista_valores_produtos)   
            dic_prod["quatis"] = statistics.quantiles(lista_valores_produtos,method='exclusive') 
            return dic_prod
        else:
            return {}
    except:
        return {}
def extrairDados(site,pesquisa_produto):
    global palavras_Proibidass, dados_bruto
    list_inf_site = []    
    reg_loja = re.compile(r"[0-9a-zA-z]{1,}[^(\.br)][^(\.com)]")
    reg_monetario = re.compile(r"[\d{1,},\d{2,2}]")
    reg_excluir_virgula = re.compile(r"[^\.]")
    reg_ajust_monetario = re.compile(r"^(\d+\.\d{2})")
    produtos = site.find_all("div",attrs={'class':'sh-dgr__gr-auto'})  
    palavra_procurada = pesquisa_produto
    try:
            lista_palavras_proibidas =  palavras_Proibidass
            print(palavras_Proibidass)
            for prod in produtos:
                    print(prod.find("span",{'class':'QIrs8'}))
                    nome_produto =  "".join(re.findall(palavra_procurada.lower(), ("".join(prod.find("h3",{'class':'tAxDx'}).get_text()).lower())))
                    valor_produto = float("".join(reg_ajust_monetario.findall(re.sub(",",".",("".join(reg_monetario.findall(("".join(reg_excluir_virgula.findall(prod.find("div",{'class':'XrAfOe'}).get_text()))))))))))
                    loja_produto = "".join(reg_loja.findall(prod.find("div",{'class':'aULzUe'}).get_text()))
                    if len(lista_palavras_proibidas) and nome_produto :
                        list_inf_site.append({"valorProduto":valor_produto,"lojaProduto":loja_produto,"nomeProduto":"".join(prod.find("h3",{'class':'tAxDx'}).get_text()).lower()})  
                    if len(lista_palavras_proibidas)>0 and nome_produto:
                        for  listpalpro in lista_palavras_proibidas:
                            if listpalpro not in  nome_produto:
                                list_inf_site.append({"valorProduto":valor_produto,"lojaProduto":loja_produto,"nomeProduto":"".join(prod.find("h3",{'class':'tAxDx'}).get_text()).lower()}) 
            return list_inf_site
    except:  
        print("Erro ao trazer os dados.")  
def boxPlot(dadosRecolhido):
    # Criar o gráfico de boxplot
    dadosRecolhidoLista = []
    for valor in dadosRecolhido:
        dadosRecolhidoLista.append(valor["valorProduto"])
    print(dadosRecolhidoLista)
    plt.boxplot(dadosRecolhidoLista,patch_artist=True, boxprops=dict(facecolor='lightblue'))
    plt.title('Boxplot do Produto')
    plt.ylabel('Preços do Produto')
    # Mostrar o gráfico
    plt.show()

continua = 1
pesquisa_produto = input("Entre com o produto que deseja pesquisar: \n")
dados_bruto = fazer_pesquisa(pesquisa_produto)

palavras_Proibidass = [] 
while continua == 1:
     pesquisa_proi_produto = input("Entre com a palavra proibida que deseja nao ter na pesquisa: \n")
     palavras_Proibidass.append(pesquisa_proi_produto)
     continuar_novamente = input("Deseja continuar. Digite 1 ou um caso queira continuar e qualquer outro caracter se desejar sair.\n")
     if (continuar_novamente == "1" or continuar_novamente == "um"):
        continua = 1
     else:
        continua = 0
        break   
dados = extrairDados(dados_bruto,pesquisa_produto)
print(f"Tamanho da amostra foi de {len(dados)}.")
print(dados)
print("Os dados recolhidos foram os seguintes:") 
parametros_estatisticos = analise_Estatistica(dados)
print(parametros_estatisticos)
boxPlot(dados)


