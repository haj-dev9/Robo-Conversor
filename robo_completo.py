import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

print("1. Buscando cotações ao vivo na API...")

url_api = "https://economia.awesomeapi.com.br/last/GBP-BRL,GBP-USD"
resposta = requests.get(url_api).json()

cotacao_libra_real = float(resposta['GBPBRL']['bid'])
cotacao_libra_dolar = float(resposta['GBPUSD']['bid'])

print("2. Iniciando o robô navegador...")
navegador = webdriver.Chrome()
navegador.maximize_window()
navegador.get("https://books.toscrape.com/")
time.sleep(2)

livros = navegador.find_elements(By.CSS_SELECTOR, "article.product_pod")

lista_titulos = []
lista_precos_libra = []
lista_precos_dolar = []
lista_precos_real = []

print("3. Extraindo dados e calculando conversões...")
for livro in livros[:5]:
    titulo = livro.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("title")
    preco_texto = livro.find_element(By.CSS_SELECTOR, ".price_color").text
    
    preco_original = float(preco_texto[1:])
    
    preco_em_real = preco_original * cotacao_libra_real
    preco_em_dolar = preco_original * cotacao_libra_dolar
    
    lista_titulos.append(titulo)
    lista_precos_libra.append(preco_original)
    
    lista_precos_real.append(round(preco_em_real, 2))
    lista_precos_dolar.append(round(preco_em_dolar, 2))

navegador.quit()

print("4. Gerando a planilha inteligente...")
dados_finais = {
    "Título": lista_titulos,
    "Preço Original (£)": lista_precos_libra,
    "Preço Convertido (US$)": lista_precos_dolar,
    "Preço Convertido (R$)": lista_precos_real
}

tabela = pd.DataFrame(dados_finais)
tabela.to_excel("livros_multimoedas.xlsx", index=False)
print("SUCESSO! O arquivo 'livros_multimoedas.xlsx' está pronto.")