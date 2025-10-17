import pandas as pd
import matplotlib.pyplot as plt
import io


try:
    df = pd.read_csv("data.csv")
except FileNotFoundError:
    print("ERRO: O arquivo 'data.csv' não foi encontrado. Verifique o caminho.")
    exit()



range_x = df['pos_x'].max() - df['pos_x'].min()
range_y = df['pos_y'].max() - df['pos_y'].min()

print(f"Variação em X (Range): {range_x}")
print(f"Variação em Y (Range): {range_y}")


plt.figure(figsize=(12, 6))


plt.plot(df['t'], df['pos_x'], label='Posição X', color='blue')




plt.plot(df['t'], df['pos_y'], label='Posição Y', color='red', linestyle='--')

plt.title('Comparação da Variação de Posição X e Posição Y ao Longo do Tempo')
plt.xlabel('Tempo (t)')
plt.ylabel('Posição (Coordenada)')
plt.legend()
plt.grid(True)
plt.show()