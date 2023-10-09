# Importação das bibliotecas necessárias
import requests  # Para fazer requisições HTTP
from bs4 import BeautifulSoup  # Para fazer scraping do HTML
import re  # Para usar expressões regulares
import pandas as pd  # Para trabalhar com dataframes
import math  # Para operações matemáticas

# URL do site a ser acessado
url = 'https://www.kabum.com.br/espaco-gamer/cadeiras-gamer'

# Configuração do cabeçalho para simular um navegador
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
}

# Realiza a requisição para o site
site = requests.get(url, headers=headers)

# Criação da sopa (objeto BeautifulSoup) para analisar o conteúdo HTML
soup = BeautifulSoup(site.content, 'html.parser')

# Extrai a quantidade de itens disponíveis da página
qtd_itens = soup.find('div', id='listingCount').get_text().strip()

# Encontra a posição do primeiro espaço para extrair a quantidade
index = qtd_itens.find(' ')

# Obtém a quantidade de itens
qtd = qtd_itens[:index]

# Imprime a quantidade de itens
print(qtd)

# Calcula o número da última página
ultima_pagina = math.ceil(int(qtd) / 20)

# Dicionário para armazenar informações dos produtos
dic_produtos = {'marca': [], 'preco': []}

# Itera sobre as páginas para coletar informações dos produtos
for i in range(1, ultima_pagina + 1):
    # Constrói a URL da página atual
    url_pag = f'https://www.kabum.com.br/espaco-gamer/cadeiras-gamer?page_number={i}&page_size=20&facet_filters=&sort=most_searched'
    site = requests.get(url_pag, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    produtos = soup.find_all('div', class_=re.compile('productCard'))

    # Itera sobre os produtos da página atual
    for produto in produtos:
        # Extrai a marca e o preço do produto
        marca = produto.find('span', class_=re.compile('nameCard')).get_text().strip()
        preco = produto.find('span', class_=re.compile('priceCard')).get_text().strip()

        # Imprime a marca e o preço do produto
        print(marca, preco)

        # Armazena a marca e o preço no dicionário de produtos
        dic_produtos['marca'].append(marca)
        dic_produtos['preco'].append(preco)

    # Imprime a URL da página atual
    print(url_pag)

# Cria um DataFrame a partir do dicionário de produtos
df = pd.DataFrame(dic_produtos)

# Salva o DataFrame em um arquivo Excel
df.to_excel('arquivo.xlsx')
