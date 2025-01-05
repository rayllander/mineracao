import pandas as pd

# Carregar o arquivo CSV (corrigir o delimitador)
file_path = "resultado_preliminar.csv"  # Substitua pelo caminho correto
data = pd.read_csv(file_path, sep=",")  # Alterado para vírgula como separador

# Mostrar os nomes das colunas para verificar a correção
print("Colunas do arquivo CSV:", data.columns.tolist())

# Padronizar os nomes das colunas (remover espaços extras)
data.columns = data.columns.str.strip()

# Função auxiliar para determinar gênero pelo nome
def determinar_genero(nome):
    nome = nome.split()[0].lower()
    if nome.endswith(("a", "e")):  # Aproximação simples para nomes femininos
        return "Feminino"
    return "Masculino"

# Adicionar coluna de gênero
data["Gênero"] = data["Candidato(a)"].apply(determinar_genero)

# Total de inscritos por curso
inscritos_por_curso = data["Curso"].value_counts()

# Percentual de homens e mulheres por curso
percentual_genero = data.groupby("Curso")["Gênero"].value_counts(normalize=True).unstack() * 100

# Filtrar mulheres negras
if "Opção de Participação" in data.columns:
    mulheres_negras = data[(data["Gênero"] == "Feminino") & (data["Opção de Participação"].str.contains("Negro", case=False))]
    percentual_mulheres_negras = (len(mulheres_negras) / len(data)) * 100
else:
    mulheres_negras = None
    percentual_mulheres_negras = "Dados de participação não encontrados no CSV."

# Curiosidade: Curso com mais inscritos
curiosidade = data["Curso"].value_counts().idxmax()  # Curso com mais inscritos

# Salvar os resultados em um arquivo de texto
output_text_path = "resultados_mineracao.txt"
with open(output_text_path, "w", encoding="utf-8") as f:
    f.write("### Resultados da Mineração de Dados ###\n\n")
    f.write("Quantidade de inscritos por curso:\n")
    f.write(inscritos_por_curso.to_string())
    f.write("\n\nPercentual de gênero por curso:\n")
    f.write(percentual_genero.to_string())
    if mulheres_negras is not None:
        f.write(f"\n\nPercentual de mulheres negras inscritas: {percentual_mulheres_negras:.2f}%\n")
    else:
        f.write("\n\nPercentual de mulheres negras inscritas: Dados de participação não encontrados no CSV.\n")
    f.write(f"\nCuriosidade: O curso com mais inscritos é '{curiosidade}'.\n")
    f.write("\n\n### Fim dos resultados ###")

print(f"\nResultados salvos no arquivo '{output_text_path}'.")
