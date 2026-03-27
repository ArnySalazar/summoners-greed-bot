\# 🎮 Summoners Greed Bot



Bot automatizado para farmear recursos en Summoners Greed usando visión por computadora con YOLOv8.



\## ¿Qué hace?

\- Detecta automáticamente las pantallas del juego

\- Farmea JR Normal automáticamente

\- Acepta recompensas del monitor/vendedor

\- Registra todas las acciones en un log



\## Requisitos

\- Python 3.11+

\- Android con depuración USB activada

\- ADB instalado



\## Instalación

```bash

git clone https://github.com/tuusuario/summoners-greed-bot

cd summoners-greed-bot

pip install -r requirements.txt

```



\## Uso

```bash

\# Paso 1 - Recolectar datos

python src/capturador.py



\# Paso 2 - Etiquetar imágenes

\# Usar LabelImg (ver docs/etiquetado.md)



\# Paso 3 - Entrenar modelo

python src/entrenar.py



\# Paso 4 - Correr bot

python src/bot.py

```



\## Estructura

```

summoners-greed-bot/

├── dataset/

│   ├── raw/          # Capturas sin etiquetar

│   ├── labeled/      # Capturas etiquetadas

│   ├── train/        # Dataset de entrenamiento

│   └── val/          # Dataset de validación

├── models/           # Modelos entrenados

├── src/              # Código fuente

├── logs/             # Logs del bot

└── docs/             # Documentación

```



\## Clases detectadas

\- `menu` - Pantalla de selección de mapa

\- `monstruos` - Pantalla de configuración

\- `bonus` - Popup del monitor/vendedor

\- `recibiste` - Popup de recompensa recibida

\- `continua` - Pantalla de victoria



\## Contribuir

¡Las contribuciones son bienvenidas! Ver docs/contribuir.md



\## Disclaimer

Este bot es para uso educativo. Úsalo bajo tu propio riesgo.

