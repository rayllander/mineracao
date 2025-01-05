import re
import csv
from PyPDF2 import PdfReader


def inferir_genero(nome):
    feminino = ["A", "E", "I"]  
    masculino = ["O", "U"]
    ultima_letra = nome.split()[-1][-1].upper()
    if ultima_letra in feminino:
        return "Feminino"
    elif ultima_letra in masculino:
        return "Masculino"
    return "Indeterminado"


def processar_pdf(pdf_path, csv_path):
    try:
        reader = PdfReader(pdf_path)
        linhas = []

        print("Extraindo texto do PDF...")
        for i, page in enumerate(reader.pages):
            print(f"Processando página {i + 1}...")
            texto = page.extract_text()
            
            curso_match = re.search(r"(Anápolis|Caldas Novas|Jaraguá|Luziânia).+?\s*-\s*(.+)", texto)
            curso = curso_match.group(2).strip() if curso_match else "Curso Não Identificado"

            for match in re.finditer(r"([A-Z\s]+)\s+(\*\*\*.\d{3}.\d{3}-\*\*)", texto):
                nome = match.group(1).strip()
                documento = match.group(2).strip()
                genero = inferir_genero(nome)
                linhas.append([curso, nome, documento, genero])

        print("Salvando resultados no arquivo CSV...")
        with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Curso", "Nome", "Documento", "Gênero"])
            writer.writerows(linhas)
        print(f"Arquivo CSV gerado com sucesso em: {csv_path}")
    except Exception as e:
        print(f"Erro ao processar o PDF: {e}")


pdf_path = r"C:\Users\rayll\Downloads\ueg.pdf"
csv_path = r"C:\Users\rayll\Downloads\resultado.csv"


processar_pdf(pdf_path, csv_path)
