import subprocess
import os
import sys

clase = sys.argv[1] if len(sys.argv) > 1 else "misc"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(ROOT, 'dataset', 'clasificado', clase)
os.makedirs(DEST, exist_ok=True)

contador = len(os.listdir(DEST)) + 1

print(f"Capturando para clase: {clase}")
print(f"Guardando en: {DEST}")
print("Presiona ENTER para capturar, Q+ENTER para salir")

while True:
    tecla = input(f"[{contador}] Listo? > ")
    if tecla.lower() == 'q':
        print(f"Listo! Total: {contador-1} capturas")
        break
    
    filename = f"manual_{clase}_{contador:03d}.png"
    ruta = os.path.join(DEST, filename)
    
    subprocess.run(["adb", "shell", "screencap", "-p", f"/sdcard/s.png"], capture_output=True)
    subprocess.run(["adb", "pull", f"/sdcard/s.png", ruta], capture_output=True)
    
    print(f"✅ Guardado: {filename}")
    contador += 1