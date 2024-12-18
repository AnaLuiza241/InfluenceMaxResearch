import pandas as pd
import matplotlib.pyplot as plt

pasta = 'gnn-edge-betweenness/csv_results/'
# Lista de arquivos CSV e suas respectivas redes
files = {
    "Rede 1": f"{pasta}network_1_betweenness.csv",
    "Rede 2": f"{pasta}network_2_betweenness.csv",
    "Rede 3": f"{pasta}network_3_betweenness.csv"
}

# Lê os dados de cada arquivo CSV
data = {rede: pd.read_csv(file) for rede, file in files.items()}

# Características a serem analisadas
features = ["betweenness", "degree", "clustering"]

# Criar gráficos para cada característica
for feature in features:
    plt.figure(figsize=(14, 6))

    for i, (rede, df) in enumerate(data.items()):
        plt.subplot(1, 3, i + 1)  # Subplots para as 3 redes
        plt.hist(df[feature], bins=10, alpha=0.7, color=f"C{i}")
        plt.title(f"{rede} - {feature.capitalize()}")
        plt.xlabel(feature.capitalize())
        plt.ylabel("Frequência")

    plt.tight_layout()
    
    # Ajustar o título para que não se sobreponha às subplots
    plt.subplots_adjust(top=0.85)  # Ajusta o topo da figura para deixar mais espaço para o título
    plt.suptitle(f"Distribuição de {feature.capitalize()} nas Redes", fontsize=16)

    # Salvar o gráfico como um arquivo PNG
    plt.savefig(f"distribuicao_{feature}.png")
    plt.close()  # Fecha a figura após salvar
