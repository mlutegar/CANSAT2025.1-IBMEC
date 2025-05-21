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

# Pair Plot (Gráfico de Pares) para Variáveis Numéricas
sns.pairplot(df[['Velocidade (m/s)', 'Distancia (m)', 'Delta tempo', 'Tempo total emissor', 'Tempo total receptor']])
plt.suptitle('Gráfico de Pares das Variáveis Numéricas', y=1.02)
plt.show()
