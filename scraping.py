from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import re, os
from pandas import DataFrame

source = "data.csv"
# Matriz de dados
data = []
work = 0
does_not_work = 0

# Executando o driver
driver = webdriver.Chrome(executable_path="C:\\ProgramData\\chocolatey\\lib\\chromedriver\\tools\\chromedriver.exe")

for number_caracter in range(65, 91):
  # Definição da variável de site a ser acessado
  url = f'http://www4.vestibular.ufjf.br/2020/notaspism2_aposrevisao__L/{chr(number_caracter)}.html'

  # Começando o driver
  driver.get(url)

  # Identificando o elemento o qual abre a parte de dados do estudante
  elements_students = driver.find_elements_by_tag_name('i')

  # Tabela atual de dados
  number_tabel = 0
  for element_student in elements_students:
    try:
      element_student.click() # Abrindo a parte de dados
      sleep(0.2)
      tbody = driver.find_elements_by_tag_name('tbody')
      
      # Após o clique, encontrando a tabela mostada
      element_html = tbody[2 + number_tabel].get_attribute("outerHTML")
      
      # Parsear conteúdo HTML
      element = BeautifulSoup(element_html, 'html.parser')
      
      # Definindo todos os elementos que contém o conteúdo desejado
      params = []
      number = 0
      rows_not_interesting = [0, 2, 3, 20, 21, 22] # Linhas não interessantes
      for date in element.findAll('tr'):
        # Se a linha for de interesse, é acrescentada
        if not number in rows_not_interesting:
          params.append(date.text)
        number += 1

      row = []

      # Adicionando o total de pontos
      points_total = str(params[0])
      row.append(float(points_total[len(points_total) - 6:].replace(",", ".")))

      number = 0
      try:
        for p in params[1:len(params)-2]:
          # Manipulando o texto
          info = None

          # Intervalo de questões objetivas
          if number <= 7 or (number >= 16 and number <= 23):
            info = int(re.findall('[0-9]', p)[0])
          
          # Intervalo de questões discursivas
          else:
            info = float(p[len(p) - 4:].replace(",", '.'))

          row.append(info)
          number += 1

        data.append(row) # Adicionando a linha na matriz de dados
        work += 1
      except:
        does_not_work += 1
      
      number_tabel += 1     

      os.system("cls")
      print(f"Funcionou: {work}")
      print(f"Não Funcinou: {does_not_work}")

    except:
      print('Não Deu')

# Definindo as linhas dos dados
index = []
for i in range(0, len(data)):
  index.append(i)

# Nome das colunas
columns = ['Total', 'PortuguêsO1', 'MatemáticaO1', 'LiteraturaO1', 'HistóriaO1', 'GeografiaO1',
          'FísicaO1', 'QuímicaO1', 'BiologiaO1', 'PortuguêsD1', 'MatemáticaD1', 'LiteraturaD1',
          'HistóriaD1', 'GeografiaD1', 'FísicaD1', 'QuímicaD1', 'BiologiaD1', 'PortuguêsO2', 
          'Matemática02', 'LiteraturaO2', 'HistóriaO2', 'GeografiaO2', 'FísicaO2', 'QuímicaO2', 
          'BiologiaO2', 'PortuguêsD2', 'MatemáticaD2', 'LiteraturaD2', 'HistóriaD2', 'GeografiaD2', 
          'FísicaD2', 'QuímicaD2', 'BiologiaD2']

# Criando o DataFrame
df = DataFrame(data,
               index=index,
               columns=columns)
# Transformando o DataFrame em .csv
df.to_csv(source, encoding='utf-8', index=False)
print('Done!')