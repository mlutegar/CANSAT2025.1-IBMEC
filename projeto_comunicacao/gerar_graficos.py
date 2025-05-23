import glob
import os

import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns # Importe seaborn para gráficos mais avançados
from mpl_toolkits.mplot3d import Axes3D

caminho = "data/"
arquivos_csv = glob.glob(os.path.join(caminho, "*.csv"))
print(f"Arquivos encontrados: {arquivos_csv}")

lista_dfs = []

for arquivo in arquivos_csv:
    df_temp = pd.read_csv(arquivo, sep=",", header=0)
    lista_dfs.append(df_temp)

df = pd.concat(lista_dfs, ignore_index=True)

# salvar csv gerado
df.to_csv("data/geral.csv", sep=",", index=False)
print(f"Dados combinados - total de linhas: {len(df)}")


# df = pd.read_csv("data/tentativa1-1500n-50m.csv", sep=",", header=0)

# # Exibir os dados carregados
# print(df)
# print(df.columns.tolist())

# Gráfico 1: Histograma da Velocidade
plt.figure()
plt.hist(df['Velocidade (m/s)'], bins=20, edgecolor='black')
plt.xlabel('Velocidade (m/s)')
plt.ylabel('Frequência')
plt.title('Distribuição da Velocidade dos Pacotes')
plt.show()

# Gráfico 2: Id da mensagem vs Velocidade
plt.figure()
plt.plot(df['Id da mensagem'], df['Velocidade (m/s)'], marker='o')
plt.xlabel('Id da mensagem')
plt.ylabel('Velocidade (m/s)')
plt.title('Velocidade por Pacote')
plt.show()

# Gráfico 3: Boxplot da Velocidade por Distância (agrupando em faixas)
df['Faixa_distancia'] = pd.cut(df['Distancia (m)'], bins=5)

plt.figure(figsize=(8,6))
df.boxplot(column='Velocidade (m/s)', by='Faixa_distancia')
plt.xlabel('Faixa de Distância (m)')
plt.ylabel('Velocidade (m/s)')
plt.title('Velocidade por Faixa de Distância')
plt.suptitle('')  # Remove o título automático do boxplot
plt.show()

# Gráfico de linha acumulada: Tempo total emissor vs Id da mensagem
plt.figure()
plt.plot(df['Id da mensagem'], df['Tempo total emissor'], marker='.', linestyle='-')
plt.xlabel('Id da mensagem')
plt.ylabel('Tempo total emissor')
plt.title('Evolução do Tempo Total Emissor por Mensagem')
plt.show()

# Gráfico de dispersão 3D: Distância vs Delta tempo vs Velocidade
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df['Distancia (m)'], df['Delta tempo'], df['Velocidade (m/s)'])
ax.set_xlabel('Distancia (m)')
ax.set_ylabel('Delta tempo')
ax.set_zlabel('Velocidade (m/s)')
ax.set_title('Distancia vs Delta tempo vs Velocidade')
plt.show()

# Gráfico de barras: Contagem de pacotes por distância arredondada
dist_counts = df['Distancia (m)'].round().value_counts().sort_index()

plt.figure()
dist_counts.plot(kind='bar')
plt.xlabel('Distancia (m) arredondada')
plt.ylabel('Número de pacotes')
plt.title('Número de pacotes por distância arredondada')
plt.show()


# --- Novos gráficos ---

# Gráfico 7: Dispersão com Cores (Id do Pacote vs. Velocidade vs. Delta Tempo)
# Criar uma coluna para representar a cor, por exemplo, o Id do Pacote
# Normalizando o Id do Pacote para usar em cores, se necessário
plt.figure(figsize=(10, 6))
scatter = plt.scatter(df['Velocidade (m/s)'], df['Delta tempo'], c=df['Id do pacote'], cmap='viridis', alpha=0.7)
plt.xlabel('Velocidade (m/s)')
plt.ylabel('Delta tempo')
plt.title('Velocidade vs Delta Tempo por Id do Pacote')
plt.colorbar(scatter, label='Id do Pacote')
plt.grid(True)
plt.show()

# Gráfico 8: Séries Temporais (Tempo Total Emissor/Receptor vs. Id da Mensagem)
plt.figure(figsize=(12, 6))
plt.plot(df['Id da mensagem'], df['Tempo total emissor'], label='Tempo Total Emissor', marker='.', linestyle='-')
plt.plot(df['Id da mensagem'], df['Tempo total receptor'], label='Tempo Total Receptor', marker='.', linestyle='--')
plt.xlabel('Id da mensagem')
plt.ylabel('Tempo (microssegundos)')
plt.title('Evolução dos Tempos de Emissor e Receptor por Mensagem')
plt.legend()
plt.grid(True)
plt.show()

# Gráfico 9: Gráfico de Calor (Correlação entre Variáveis Numéricas)
# Selecionar apenas as colunas numéricas para o mapa de calor
numeric_cols = df.select_dtypes(include=['number']).columns
correlation_matrix = df[numeric_cols].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Mapa de Calor da Correlação entre Variáveis')
plt.show()

# Gráfico de Densidade (KDE) para Velocidade por Faixa de Distância
plt.figure(figsize=(10, 6))
for faixa in df['Faixa_distancia'].unique():
    sns.kdeplot(data=df[df['Faixa_distancia'] == faixa], x='Velocidade (m/s)', label=str(faixa))
plt.xlabel('Velocidade (m/s)')
plt.ylabel('Densidade')
plt.title('Distribuição de Velocidade por Faixa de Distância')
plt.legend(title='Faixa de Distância')
plt.grid(True)
plt.show()

#  Gráfico de Violin Plot para Velocidade por Faixa de Distânci
plt.figure(figsize=(10, 6))
sns.violinplot(x='Faixa_distancia', y='Velocidade (m/s)', data=df)
plt.xlabel('Faixa de Distância (m)')
plt.ylabel('Velocidade (m/s)')
plt.title('Distribuição de Velocidade por Faixa de Distância (Violin Plot)')
plt.xticks(rotation=45)
plt.show()

# Gráfico de Linha com Média Móvel (Velocidade ao Longo do Id da Mensagem)
plt.figure(figsize=(12, 6))
df['Velocidade_media_movel'] = df['Velocidade (m/s)'].rolling(window=10).mean()
plt.plot(df['Id da mensagem'], df['Velocidade (m/s)'], label='Velocidade', alpha=0.3)
plt.plot(df['Id da mensagem'], df['Velocidade_media_movel'], label='Média Móvel (janela=10)', color='red')
plt.xlabel('Id da mensagem')
plt.ylabel('Velocidade (m/s)')
plt.title('Velocidade com Média Móvel por Id da Mensagem')
plt.legend()
plt.grid(True)
plt.show()

#  Gráfico de Barras Empilhadas (Contagem de Pacotes por Id do Pacote e Faixa de Distância)
plt.figure(figsize=(12, 6))
pivot_table = df.groupby(['Id do pacote', 'Faixa_distancia']).size().unstack(fill_value=0)
pivot_table.plot(kind='bar', stacked=True, figsize=(12, 6))
plt.xlabel('Id do Pacote')
plt.ylabel('Contagem de Pacotes')
plt.title('Contagem de Pacotes por Id do Pacote e Faixa de Distância')
plt.legend(title='Faixa de Distância')
plt.show()

# Pair Plot (Gráfico de Pares) para Variáveis Numéricas
sns.pairplot(df[['Velocidade (m/s)', 'Distancia (m)', 'Delta tempo', 'Tempo total emissor', 'Tempo total receptor']])
plt.suptitle('Gráfico de Pares das Variáveis Numéricas', y=1.02)
plt.show()

