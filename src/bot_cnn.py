"""
Bot para Summoners Greed usando CNN para detección de pantallas
Con visualización en tiempo real, estadísticas y reentrenamiento
"""
import subprocess
import time
import random
import logging
import os
import cv2
import shutil
import numpy as np
import tensorflow as tf
from datetime import datetime
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from estadisticas import registrar_run

# ============ CONFIGURACION ============
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(ROOT, 'models', 'mejor_modelo.keras')
SCREEN_PATH = os.path.join(ROOT, 'screen_bot.png')
LOG_PATH = os.path.join(ROOT, 'logs', 'bot.log')
INCIERTOS_DIR = os.path.join(ROOT, 'dataset', 'inciertos')
os.makedirs(os.path.join(ROOT, 'logs'), exist_ok=True)
os.makedirs(INCIERTOS_DIR, exist_ok=True)

CLASES = ['jugando', 'menu', 'monstruos', 'bonus', 'recibiste', 'continua', 'otros']

COORDS = {
    'jr_normal':  (218,  1962),
    'confirmar':  (540,  2316),
    'recompensa': (772,  1298),
    'aceptar':    (542,  1306),
    'continua':   (534,  1730),
}

CONFIANZA_MIN = 0.45
CONFIANZA_INCIERTA = 0.75

COLORES = {
    'jugando':   (0, 255, 0),
    'menu':      (0, 165, 255),
    'monstruos': (255, 0, 255),
    'bonus':     (0, 255, 255),
    'recibiste': (255, 165, 0),
    'continua':  (0, 255, 128),
    'otros':     (128, 128, 128),
}

# Estado global para visualizacion
ultimo_estado = 'jugando'
ultima_confianza = 0.0

# ============ LOGGING ============
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def log(msg):
    logging.info(msg)
    print(msg)

# ============ CARGAR MODELO ============
log("Cargando modelo CNN...")
modelo = load_model(MODEL_PATH)
log("Modelo cargado!")

# ============ VISUALIZACION ============
def mostrar_pantalla(tap_x=None, tap_y=None):
    img = cv2.imread(SCREEN_PATH)
    if img is None:
        return

    img_show = cv2.resize(img, (270, 600))
    scale_x = 270 / 1080
    scale_y = 600 / 2400

    color = COLORES.get(ultimo_estado, (255, 255, 255))

    cv2.rectangle(img_show, (0, 0), (270, 55), (0, 0, 0), -1)
    cv2.putText(img_show, f"Estado: {ultimo_estado}", (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)
    cv2.putText(img_show, f"Confianza: {ultima_confianza:.1%}", (10, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)

    if tap_x and tap_y:
        tx = int(tap_x * scale_x)
        ty = int(tap_y * scale_y)
        cv2.circle(img_show, (tx, ty), 12, (0, 0, 255), -1)
        cv2.circle(img_show, (tx, ty), 18, (255, 255, 255), 2)
        cv2.putText(img_show, f"TAP ({tap_x},{tap_y})", (10, 580),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

    cv2.imshow("Summoners Greed Bot", img_show)
    cv2.waitKey(1)

# ============ ADB ============
def tap(x, y):
    rx = x + random.randint(-4, 4)
    ry = y + random.randint(-4, 4)
    subprocess.run(["adb", "shell", "input", "tap", str(rx), str(ry)],
                   capture_output=True)
    log(f"TAP en ({rx}, {ry})")
    mostrar_pantalla(rx, ry)
    time.sleep(0.8)

def screenshot():
    subprocess.run(["adb", "shell", "screencap", "-p", "/sdcard/screen_bot.png"],
                   capture_output=True)
    subprocess.run(["adb", "pull", "/sdcard/screen_bot.png", SCREEN_PATH],
                   capture_output=True)

# ============ DETECCION CNN ============
def detectar_pantalla():
    global ultimo_estado, ultima_confianza
    screenshot()

    img = image.load_img(SCREEN_PATH, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predicciones = modelo.predict(img_array, verbose=0)
    clase_idx = np.argmax(predicciones[0])
    confianza = float(predicciones[0][clase_idx])
    clase = CLASES[clase_idx]

    ultimo_estado = clase
    ultima_confianza = confianza

    mostrar_pantalla()
    log(f"Detectado: {clase} ({confianza:.2%})")

    # Guardar capturas inciertas para reentrenamiento
    if CONFIANZA_MIN <= confianza <= CONFIANZA_INCIERTA:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        ruta = os.path.join(INCIERTOS_DIR, f"incierto_{clase}_{confianza:.2f}_{timestamp}.png")
        shutil.copy(SCREEN_PATH, ruta)
        log(f"⚠️ Guardado incierto: {clase} ({confianza:.2%})")

    if confianza < CONFIANZA_MIN:
        return 'jugando'

    return clase

# ============ BOT ============
def run_completa():
    bonus_count = 0
    inicio_run = time.time()

    log("Verificando menu...")
    for _ in range(5):
        estado = detectar_pantalla()
        if estado == 'menu':
            break
        time.sleep(2)
    else:
        log("No detecto menu, volviendo atras...")
        subprocess.run(["adb", "shell", "input", "keyevent", "4"],
                       capture_output=True)
        time.sleep(3)
        registrar_run(False, time.time() - inicio_run, bonus_count)
        return False

    log("Tocando JR Normal...")
    tap(*COORDS['jr_normal'])
    time.sleep(3)

    log("Esperando pantalla monstruos...")
    for _ in range(10):
        estado = detectar_pantalla()
        if estado == 'monstruos':
            log("Confirmando monstruos...")
            tap(*COORDS['confirmar'])
            time.sleep(3)
            break
        time.sleep(1)

    log("Run iniciada...")
    inicio = time.time()
    tiempo_max = 25 * 60

    while time.time() - inicio < tiempo_max:
        estado = detectar_pantalla()

        if estado == 'continua':
            log("Run completada! Tocando Continua...")
            tap(*COORDS['continua'])
            time.sleep(3)
            registrar_run(True, time.time() - inicio_run, bonus_count)
            return True

        elif estado == 'bonus':
            bonus_count += 1
            log(f"Bonus #{bonus_count} detectado! Tocando Recompensa Gratis...")
            tap(*COORDS['recompensa'])
            log("Esperando anuncio...")
            for _ in range(60):
                time.sleep(1)
                estado_inner = detectar_pantalla()
                if estado_inner == 'recibiste':
                    break

        elif estado == 'recibiste':
            log("Recibiste! Tocando Aceptar...")
            tap(*COORDS['aceptar'])
            time.sleep(2)

        elif estado == 'menu':
            log("Volvio al menu inesperadamente")
            registrar_run(False, time.time() - inicio_run, bonus_count)
            return False

        elif estado == 'jugando':
            time.sleep(3)

        else:
            time.sleep(2)

    log("Run excedio 25 minutos")
    registrar_run(False, time.time() - inicio_run, bonus_count)
    return False

# ============ MAIN ============
log("=" * 40)
log("Bot CNN iniciado. Ctrl+C para detener.")
log("=" * 40)

cv2.namedWindow("Summoners Greed Bot", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Summoners Greed Bot", 270, 600)

corridas = 0
exitosas = 0

while True:
    try:
        resultado = run_completa()
        corridas += 1
        if resultado:
            exitosas += 1
        log(f"Run #{corridas} | Exitosas: {exitosas}/{corridas}")
        time.sleep(random.uniform(2, 4))

    except KeyboardInterrupt:
        log(f"Bot detenido. Exitosas: {exitosas}/{corridas}")
        cv2.destroyAllWindows()
        break
    except Exception as e:
        log(f"Error: {e}")
        time.sleep(10)