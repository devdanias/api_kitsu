from flask import Flask, render_template
import openpyxl
import os

app = Flask(__name__)

# Caminho para o relatório
relatorios = r'C:\Projetos\APIKitsu\relatorios'
imagens = r'C:\Projetos\APIKitsu\imagens'  # Caminho para as imagens

# Função para ler os dados da planilha
def ler_planilha():
    wb = openpyxl.load_workbook(os.path.join(relatorios, 'anime_report.xlsx'))
    ws = wb.active
    dados = []
    for row in ws.iter_rows(min_row=2, values_only=True):  # Ignorar a primeira linha (cabeçalho)
        dados.append({
            'title': row[0],
            'synopsis': row[1],
            'average_rating': row[2],
            'poster_url': row[3],
            'created_at': row[4],
            'updated_at': row[5],
            'image_name': row[6]
        })
    return dados

@app.route('/')
def index():
    dados = ler_planilha()  # Lê os dados da planilha
    return render_template('index.html', animes=dados)

if __name__ == '__main__':
    app.run(debug=True)
