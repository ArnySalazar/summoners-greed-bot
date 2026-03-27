"""
Capturador de pantallas para dataset de entrenamiento.
Toma capturas cada 3 segundos mientras juegas.
"""
import subprocess
import time
import os
from datetime import datetime

# Rutas
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(ROOT, 'dataset', 'raw')
os.makedirs(DATASET_DIR, exist_ok=True)

def capturar():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"captura_{timestamp}.png"
    ruta_local = os.path.join(DATASET_DIR, filename)
    
    subprocess.run(
        ["adb", "shell", "screencap", "-p", f"/sdcard/{filename}"],
        capture_output=True
    )
    subprocess.run(
        ["adb", "pull", f"/sdcard/{filename}", ruta_local],
        capture_output=True
    )
    subprocess.run(
        ["adb", "shell", "rm", f"/sdcard/{filename}"],
        capture_output=True
    )
    return filename

def main():
    print("=" * 50)
    print("Summoners Greed Bot - Capturador")
    print("=" * 50)
    print(f"Guardando en: {DATASET_DIR}")
    print("Juega normalmente. Ctrl+C para detener.")
    print("=" * 50)

    contador = 0
    inicio = time.time()

    while True:
        try:
            filename = capturar()
            contador += 1
            elapsed = int(time.time() - inicio)
            print(f"[{elapsed}s] Captura #{contador}: {filename}")
            time.sleep(3)

        except KeyboardInterrupt:
            print(f"\nDetenido. Total capturas: {contador}")
            print(f"Tiempo total: {int(time.time()-inicio)}s")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(3)

if __name__ == "__main__":
    main()