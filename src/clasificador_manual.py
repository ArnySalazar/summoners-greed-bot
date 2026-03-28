import cv2
import os
import shutil

# Rutas
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(ROOT, 'dataset', 'raw')
CLASIFICADO_DIR = os.path.join(ROOT, 'dataset', 'clasificado')

CLASES = {
    '1': 'jugando',
    '2': 'menu',
    '3': 'monstruos',
    '4': 'bonus',
    '5': 'recibiste',
    '6': 'continua',
    '0': 'otros'
}

# Crear carpetas
for clase in CLASES.values():
    os.makedirs(os.path.join(CLASIFICADO_DIR, clase), exist_ok=True)

# Obtener imágenes sin clasificar
imagenes = [f for f in os.listdir(RAW_DIR) if f.endswith('.png')]
total = len(imagenes)

print("=" * 50)
print("Clasificador Manual - Summoners Greed")
print("=" * 50)
print("Teclas:")
for key, clase in CLASES.items():
    print(f"  {key} → {clase}")
print("  Q → Salir")
print("=" * 50)

clasificadas = 0
for i, filename in enumerate(imagenes):
    ruta = os.path.join(RAW_DIR, filename)
    img = cv2.imread(ruta)
    
    if img is None:
        continue

    # Redimensionar para mostrar
    h, w = img.shape[:2]
    img_show = cv2.resize(img, (270, 600))
    
    # Agregar texto
    cv2.putText(img_show, f"{i+1}/{total}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(img_show, "1:jugando 2:menu 3:monstruos", (10, 560),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    cv2.putText(img_show, "4:bonus 5:recibiste 6:continua 0:otros", (10, 580),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

    cv2.imshow("Clasificador", img_show)
    
    while True:
        key = cv2.waitKey(0) & 0xFF
        char = chr(key)
        
        if char == 'q':
            print(f"\nSaliendo... Clasificadas: {clasificadas}")
            cv2.destroyAllWindows()
            exit()
        
        if char in CLASES:
            clase = CLASES[char]
            destino = os.path.join(CLASIFICADO_DIR, clase, filename)
            shutil.copy(ruta, destino)
            clasificadas += 1
            print(f"[{i+1}/{total}] {filename} → {clase}")
            break

cv2.destroyAllWindows()
print(f"\nListo! Total clasificadas: {clasificadas}")