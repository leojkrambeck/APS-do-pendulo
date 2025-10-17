import cv2 as cv 
import pandas as pd 
import numpy as np 


VIDEO_PATH = 'vid4.mp4'
frame_rate = round(1/60, 2) 
data = [] 

LOWER_GREEN = np.array([35, 50, 50])  # Limite inferior do verde
UPPER_GREEN = np.array([85, 255, 255]) # Limite superior do verde




def bin(frame):
    # 1. Converte para o espaço de cores HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    # 2. Cria uma máscara que isola a cor dentro da faixa [LOWER_GREEN, UPPER_GREEN]
    mask = cv.inRange(hsv, LOWER_GREEN, UPPER_GREEN)
    
    # 3. Aplica Morfologia para Limpeza (Abertura para remover ruído)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel, iterations=1) 
    
    return mask


def cm(frame_bin):
    momentos = cv.moments(frame_bin)

    if momentos["m00"] != 0:
        center_x = int(momentos["m10"] / momentos["m00"])
        center_y = int(momentos["m01"] / momentos["m00"])
        return center_x, center_y
    else:
        return -1, -1


def capture(sec):
    cap = cv.VideoCapture(VIDEO_PATH)
    # Define a posição do vídeo em milissegundos
    cap.set(cv.CAP_PROP_POS_MSEC, sec * 1000) 
    ok, frame = cap.read()
    cap.release() 

    if ok:
        frame_bin = bin(frame.copy()) 
        center_x, center_y = cm(frame_bin)
        
        
        if center_x != -1 and center_y != -1:
            # Desenha um círculo verde (0, 255, 0) no CM
            cv.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1) 
            text = f"T: {sec:.2f}s | CM(X): {center_x} | CM(Y): {center_y}"
            cv.putText(frame, text, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            data.append({"pos_x": center_x, "pos_y": center_y, "t": sec})
            
        
        cv.imshow("Rastreamento do Pendulo (Pressione 'q' para sair)", frame)#cria a janela
        
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            return False 
            
        return True 
    
    return False 


#loop de analise dos frames

sec = 0
print(f"Iniciando rastreamento de {VIDEO_PATH}...")

cv.destroyAllWindows()

while capture(sec):
    sec += frame_rate
    sec = round(sec, 2)
    
cv.destroyAllWindows() 
print("Rastreamento concluído. Salvando dados...")

#salvamento dos dados
csv = pd.DataFrame(data)
csv.to_csv("data.csv", index = False) #manda pro data csv

print(f"Dados salvos em data.csv. Total de {len(data)} pontos.")