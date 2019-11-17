import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import csv
import os

LIST_URL = "https://www.camara.leg.br/internet/agencia/infograficos-html5/DeputadosEleitos/index.html"

def scrape():
    with open(os.path.join('data', 'deputies_names.csv'), mode='w') as output_file:
        # Initalizing the csv output
        writer = csv.writer(output_file)
        writer.writerow(['name','party'])
        # Fetching the page
        response = requests.get(LIST_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        for line in soup.findAll('tr', attrs={'class': None}):
            line_soup = BeautifulSoup(str(line), 'html.parser')
            deputado = []
            for element in line_soup.findAll('td', attrs={'class': None}):
                deputado.append(element.get_text())
            if deputado:
                # Writing the name and party the csv
                writer.writerow(deputado)
                print(deputado)

def main():
    scrape()

if __name__ == '__main__':
    main()