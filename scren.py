import cv2
import numpy as np
import pyautogui
 
 # hacer prueba y error hasta encontrar las coordenadas correctas.
while True:
     # Coordenadas de la pantalla del juego
     screenshot = pyautogui.screenshot(region=(330, 100, 640, 350))
     screenshot = np.array(screenshot)
     screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
     cv2.imshow("screenshot", screenshot)
     if cv2.waitKey(1) & 0xFF == 27:
          break
cv2.destroyAllWindows()