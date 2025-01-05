import pdfplumber
import pandas as pd
import re

# Caminho do arquivo PDF
pdf_path = r"C:\Users\rayll\Downloads\2024_05_29_IF_GOIANO_PROFESSOR_resultado_preliminar_inscricoes_homologados.pdf"

# Saída do arquivo CSV
csv_output_path = r"C:\Users\rayll\Downloads\resultado_preliminar.csv"

def extrair_dados_com_texto():
    try:
        print("Abrindo o PDF...")
        dados = []

        # Abre o PDF e extrai o texto página por página
        with pdfplumber.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                print(f"Processando texto da página {page_number}...")
                texto = page.extract_text()

                # Processa linhas de texto para extrair os dados das tabelas
                if texto:
                    for linha in texto.split("\n"):
                        # Ajusta a regex para capturar o nome do curso até encontrar a opção de participação
                        match = re.match(r"^(.*?)(\d{10})(.*?)(?=\s(AC|Negro|PcD|Indigena|Quilombola))", linha)
                        if match:
                            candidato, inscricao, curso, opcao = match.groups()

                            # Limpeza das variáveis
                            candidato = candidato.strip()
                            inscricao = inscricao.strip()
                            curso = curso.strip()
                            opcao = opcao.strip()

                            # Corrige a separação de dados
                            dados.append([candidato, inscricao, curso, opcao])

        # Exibe os dados extraídos para depuração
        print("Dados extraídos (primeiras linhas):")
        for linha in dados[:5]:
            print(linha)

        # Converte os dados para um DataFrame do pandas
        if dados:
            print("Formatando dados...")
            df = pd.DataFrame(dados, columns=["Candidato(a)", "Inscrição", "Curso", "Opção de Participação"])

            # Salva o DataFrame em um arquivo CSV
            print("Salvando em CSV...")
            df.to_csv(csv_output_path, index=False, encoding="utf-8")
            print(f"Arquivo salvo com sucesso em: {csv_output_path}")
        else:
            print("Nenhum dado estruturado encontrado no PDF.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    extrair_dados_com_texto()
