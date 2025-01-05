import pandas as pd


file_path = r"C:\Users\rayll\Downloads\resultado.csv"  # Ajuste o caminho conforme necessário
data = pd.read_csv(file_path)


inscritos_por_vaga = data['Curso'].value_counts()


data['Genero'] = data['Gênero'].str.strip().str.capitalize() 
percentual_genero = data.groupby('Curso')['Genero'].value_counts(normalize=True) * 100


curiosidade = "O curso com mais inscritos foi '{}' com {} candidatos.".format(
    inscritos_por_vaga.idxmax(), inscritos_por_vaga.max()
)

output_file = r"C:\Users\rayll\Downloads\relatorio_concurso.txt"
with open(output_file, "w", encoding="utf-8") as file:
    file.write("Relatório do Concurso UEG\n")
    file.write("="*40 + "\n")
    file.write("\n1. Quantidade de inscritos por vaga:\n")
    file.write(inscritos_por_vaga.to_string())
    file.write("\n\n2. Percentual de homens e mulheres por vaga:\n")
    file.write(percentual_genero.to_string())
    file.write("\n\n[CURIOSIDADE]\n")
    file.write(curiosidade)

print(f"Relatório gerado em: {output_file}")
