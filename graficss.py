import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
import seaborn as sb

# Função do movimento harmônico amortecido (MHA)
def mha(t, A, b, w, phi, C): 
    # Retorna: Amplitude * e^(-b*t) * cos(w*t + phi) + C (offset/centro)
    return (A * np.exp(-b * t) * np.cos(w * t + phi) + C)


data = pd.read_csv("data.csv")
#le os dados de csv


pos_col = "pos_x" 


max_val = data[pos_col].max()
data["norm_pos"] = np.divide(data[pos_col], max_val)


initial_guess = [1, 0.05, 0.5, 0, 0.5]#chute inicial de normalizacao e otimizacao da curva



try:
    vals, pcov = curve_fit(mha, data["t"], data["norm_pos"], p0=initial_guess)
except RuntimeError:
    print("ERRO: O ajuste (curve_fit) falhou. Verifique se há oscilação suficiente nos dados.")
    vals = initial_guess 


A, b, w, phi, C = vals
w0 = np.sqrt(w**2 + b**2) # Frequência natural (não amortecida)
fator_de_qualidade = w0 / (2 * b)


data["fit"] = mha(data["t"], *vals)

print("Parâmetros (A, b, w, phi, C):", vals)
print(f"Fator de Qualidade (Q): {fator_de_qualidade:.4f}")

# Plotagem
sb.scatterplot(data=data, x="t", y="norm_pos", label="Dados Rastreados", s=10) # Pontos originais
sb.lineplot(data=data, x="t", y="fit", label="Ajuste MHA", color='red')    # Linha do fit
plt.title(f"Oscilação do Pêndulo (Q = {fator_de_qualidade:.2f})")
plt.xlabel("Tempo (s)")
plt.ylabel(f"Posição Horizontal (Normalizada)")
plt.legend()
plt.show()