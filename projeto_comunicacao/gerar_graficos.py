import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from io import StringIO

df = pd.read_csv("data/tentativa1-1500n-12m.csv", sep=",", header=0)

# Exibir os dados carregados
print(df)
print(df.columns.tolist())

# Gráfico 1: Distância vs Delta tempo
plt.figure()
plt.scatter(df['Distancia (m)'], df['Delta tempo'])
plt.xlabel('Distancia (m)')
plt.ylabel('Delta tempo')
plt.title('Distancia vs Delta tempo')
plt.show()

# Gráfico 2: Id da mensagem vs Velocidade
plt.figure()
plt.plot(df['Id da mensagem'], df['Velocidade (m/s)'], marker='o')
plt.xlabel('Id da mensagem')
plt.ylabel('Velocidade (m/s)')
plt.title('Velocidade por Pacote')
plt.show()

# Gráfico 3: Id da mensagem vs Tempo total receptor
plt.figure()
plt.plot(df['Id da mensagem'], df['Tempo total receptor'])
plt.xlabel('Id da mensagem')
plt.ylabel('Tempo total receptor')
plt.title('Tempo receptor por Pacote')
plt.show()
