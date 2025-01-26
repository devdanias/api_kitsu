import requests
import urllib.parse
import json
import os
import openpyxl
from datetime import datetime

relatorios = r'C:\Projetos\APIKitsu\relatorios'
imagens = r'C:\Projetos\APIKitsu\imagens' 
os.makedirs(relatorios, exist_ok=True)
os.makedirs(imagens, exist_ok=True)  

# Base URL da API
base_url = 'https://private-amnesiac-7fa337-kitsu.apiary-proxy.com/api/edge/anime'
params = {
    'filter[categories]': 'adventure',  
    'page[limit]': 20,                 
    'page[offset]': 0                  
}

url = f"{base_url}?{urllib.parse.urlencode(params)}"

# Criando o objeto de requisição com cabeçalhos personalizados
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
}

def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        return date_obj.strftime('%d/%m/%Y')
    except ValueError:
        return 'N/A'

def download_image(image_url, image_name):
    try:
        # Fazendo a requisição da imagem
        response = requests.get(image_url, headers=headers, stream=True)
        response.raise_for_status()  
        image_path = os.path.join(imagens, image_name)
        with open(image_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Imagem salva: {image_name}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar a imagem {image_name}: {e}")

try:
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Animes"
    ws.append(['Title', 'Synopsis', 'Average Rating', 'Poster Image URL', 'Created At', 'Updated At', 'Image Saved'])

    for item in data['data']:
        attributes = item['attributes']
        title = attributes['canonicalTitle']
        synopsis = attributes['synopsis']
        average_rating = attributes.get('averageRating', 'N/A')  
        poster_url = attributes['posterImage']['original']
        created_at = format_date(attributes['createdAt'])  
        updated_at = format_date(attributes['updatedAt'])  

        image_name = f"{title.replace(' ', '_')}.jpg"
        download_image(poster_url, image_name)

        ws.append([title, synopsis, average_rating, poster_url, created_at, updated_at, image_name])

    report_file = os.path.join(relatorios, 'anime_report.xlsx')
    wb.save(report_file)
    print(f"Relatório salvo em: {report_file}")

except requests.exceptions.RequestException as e:
    print(f"Erro na requisição HTTP: {e}")
except Exception as e:
    print(f"Erro inesperado: {e}")
