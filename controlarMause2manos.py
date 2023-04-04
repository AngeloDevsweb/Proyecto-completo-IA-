import cv2  # Se importa la biblioteca OpenCV para procesamiento de imágenes
import mediapipe as mp  # Se importa la biblioteca Mediapipe para el reconocimiento de gestos de la mano
import numpy as np  # Se importa la biblioteca NumPy para operaciones matemáticas con arrays
import pyautogui  # Se importa la biblioteca PyAutoGUI para controlar el cursor del mouse y realizar clics

mp_drawing = mp.solutions.drawing_utils  # Se utiliza la función drawing_utils de Mediapipe para dibujar sobre la imagen procesada
mp_hands = mp.solutions.hands  # Se utiliza la función hands de Mediapipe para el reconocimiento de gestos de la mano

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Se inicializa la cámara web para capturar video en tiempo real

Color_Puntero = (50, 250, 0)  # Se define el color del cursor del mouse

#Puntos de la pantalla del Juego
Pantalla_del_Juego_X_inicio = 230  # Se define la coordenada X inicial del área de juego
Pantalla_del_Juego_Y_inicio = 100  # Se define la coordenada Y inicial del área de juego
Pantalla_del_Juego_X_Fin = 230 + 640  # Se define la coordenada X final del área de juego
Pantalla_del_Juego_Y_Fin = 100 + 350  # Se define la coordenada Y final del área de juego

aspect_ratio_screen = (Pantalla_del_Juego_X_Fin - Pantalla_del_Juego_X_inicio) / (Pantalla_del_Juego_Y_Fin - Pantalla_del_Juego_Y_inicio)  # Se calcula la relación de aspecto del área de juego
print("aspect_ratio_screen:", aspect_ratio_screen)  # Se imprime la relación de aspecto del área de juego

Margen_X_Y = 50  # Se define el tamaño del margen de la ventana delimitadora

def calcular_distancia(x1, y1, x2, y2):  # Se define la función para calcular la distancia euclidiana entre dos puntos
    p1 = np.array([x1, y1])  # Se crea un array NumPy con las coordenadas del primer punto
    p2 = np.array([x2, y2])  # Se crea un array NumPy con las coordenadas del segundo punto
    return np.linalg.norm(p1 - p2)  # Se calcula la distancia euclidiana entre los dos puntos y se retorna el resultado


def detectar_dedo_abajo(hand_landmarks):  # Se define la función para detectar si el dedo índice está hacia abajo o no
    dedo_abajo = False  # Se inicializa la variable booleana en False
    color_base = (0, 0, 255)  # Se define el color de la base del dedo
    color_indice = (250, 250, 0)  # Se define el color del dedo índice

    x_base1 = int(hand_landmarks.landmark[0].x * width)  # Se obtiene la coordenada X de la primera articulación de la base del dedo
    y_base1 = int(hand_landmarks.landmark[0].y * height) # Se obtiene la coordenada Y de la primera articulación de la base del dedo
    
    x_base2 = int(hand_landmarks.landmark[9].x * width) # Se obtiene la coordenada X de la segunda articulación de la base del dedo
    y_base2 = int(hand_landmarks.landmark[9].y * height) # Se obtiene la coordenada Y de la segunda articulación de la base del dedo

    x_indice = int(hand_landmarks.landmark[8].x * width) # Se obtiene la coordenada X del extremo del dedo índice
    y_indice = int(hand_landmarks.landmark[8].y * height) # Se obtiene la coordenada Y del extremo del dedo índice
    
    x_medio = int(hand_landmarks.landmark[12].x * width) 
    y_medio = int(hand_landmarks.landmark[12].y * height) 
    
    x_anular = int(hand_landmarks.landmark[16].x * width) 
    y_anular = int(hand_landmarks.landmark[16].y * height) 

    x_meñique = int(hand_landmarks.landmark[20].x * width) 
    y_meñique = int(hand_landmarks.landmark[20].y * height)
    
    x_pulgar = int(hand_landmarks.landmark[4].x * width) 
    y_pulgar = int(hand_landmarks.landmark[4].y * height)  

    distancia_base = calcular_distancia(x_base1, y_base1, x_base2, y_base2) # Se calcula la distancia entre las dos articulaciones de la base del dedo
    distancia_base_indice = calcular_distancia(x_base1, y_base1, x_indice, y_indice) # Se calcula la distancia entre la primera articulación de la base del dedo y el extremo del dedo índice
    
    
    if distancia_base_indice < distancia_base: # Si la distancia entre la primera articulación de la base del dedo y el extremo del dedo índice es menor que la distancia entre las dos articulaciones de la base del dedo
        dedo_abajo = True # Se cambia el valor de la variable booleana a True
        color_base = (50, 250, 0) # Se cambia el color de la base del dedo a verde
        color_indice = (50, 250, 0) # Se cambia el color del dedo índice a verde

    cv2.circle(output, (x_base1, y_base1), 5, color_base, 2) # Se dibuja un círculo en la primera articulación de la base del dedo con el color correspondiente
    cv2.circle(output, (x_indice, y_indice), 5, color_indice, 2) # Se dibuja un círculo en el extremo del dedo índice con el color correspondiente
    cv2.line(output, (x_base1, y_base1), (x_base2, y_base2), color_base, 2) # Se dibuja una línea desde la primera articulación de la base del dedo hasta la segunda articulación con el color correspondiente
    cv2.line(output, (x_base1, y_base1), (x_indice, y_indice), color_indice, 3) # Se dibuja una línea desde la primera articulación de la base del dedo
    
    cv2.line(output, (x_base1, y_base1), (x_medio, y_medio), color_indice, 2)
    cv2.line(output, (x_base1, y_base1), (x_anular, y_anular), color_indice, 2)
    cv2.line(output, (x_base1, y_base1), (x_meñique, y_meñique), color_indice, 2)
    cv2.line(output, (x_base1, y_base1), (x_pulgar, y_pulgar), color_indice, 2)

    return dedo_abajo

with mp_hands.Hands(
    static_image_mode=False,                 # para que se capturen los frames de la cámara en tiempo real
    max_num_hands=2,                         #para detectar 2 manos
    min_detection_confidence=0.5) as hands:  # para establecer el umbral mínimo de confianza de detección

    
    while True: # Inicia un loop infinito
        
        ret, frame = cap.read() # Lee un frame de la cámara    
        if ret == False:    # Si no hay más frames que leer, rompe el loop
            break
       
        height, width, _ = frame.shape # Obtiene el alto y ancho del frame    
        frame = cap.read()[1]  

        # Dibuja un rectángulo en el frame que simula el área de juego
        area_ancho = width - Margen_X_Y * 2
        area_alto = int(area_ancho / aspect_ratio_screen)
        aux_image = np.zeros(frame.shape, np.uint8)
        aux_image = cv2.rectangle(aux_image, (Margen_X_Y, Margen_X_Y), (Margen_X_Y + area_ancho, Margen_X_Y +area_alto), (100, 100, 0), -1)
        
        output = cv2.addWeighted(frame, 1, aux_image, 0.7, 0)   # Une el frame original y el rectángulo dibujado     
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convierte el frame a RGB       
        resultado = hands.process(frame_rgb)  # Procesa la imagen para detectar manos
        
        if resultado.multi_hand_landmarks is not None:
                # Si se detectaron dos manos
            if len(resultado.multi_hand_landmarks) == 2:

                # Selecciona la mano para hacer clic izquierdo en el botón del mouse (la primera mano detectada)
                mano_click = resultado.multi_hand_landmarks[1]
                # Selecciona la mano para mover el cursor del mouse (la segunda mano detectada)
                mano_cursor = resultado.multi_hand_landmarks[0]
                
                # Obtiene la posición de la punta del dedo índice de la mano de movimiento del mouse
                x = int(mano_cursor.landmark[9].x * width)
                y = int(mano_cursor.landmark[9].y * height)
                
                # Convierte las coordenadas del frame a coordenadas en la pantalla de juego
                xm = np.interp(x, (Margen_X_Y, Margen_X_Y + area_ancho), (Pantalla_del_Juego_X_inicio, Pantalla_del_Juego_X_Fin))
                ym = np.interp(y, (Margen_X_Y, Margen_X_Y + area_alto), (Pantalla_del_Juego_Y_inicio, Pantalla_del_Juego_Y_Fin))              
                pyautogui.moveTo(int(xm), int(ym))  # Mueve el mouse a la posición de la mano
                
                # Si se detecta que el dedo índice de la mano de clic está levantado
                if detectar_dedo_abajo(mano_click):
                    pyautogui.click()   # Simula un clic izquierdo del mouse               
                cv2.circle(output, (x, y), 10, Color_Puntero, 3)  # Dibuja un círculo en la posición de la mano en el frame
                cv2.circle(output, (x, y), 5, Color_Puntero, -1)

            cv2.imshow('Camara', output)    
            if cv2.waitKey(1) & 0xFF == 27:
                break
cap.release()
cv2.destroyAllWindows()