import json
import os
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATS_PATH = os.path.join(ROOT, 'logs', 'estadisticas.json')
os.makedirs(os.path.join(ROOT, 'logs'), exist_ok=True)

def cargar_stats():
    if os.path.exists(STATS_PATH):
        with open(STATS_PATH, 'r') as f:
            return json.load(f)
    return {
        'runs_completadas': 0,
        'runs_fallidas': 0,
        'bonus_recibidos': 0,
        'tiempo_total_minutos': 0,
        'historial': []
    }

def guardar_stats(stats):
    with open(STATS_PATH, 'w') as f:
        json.dump(stats, f, indent=2)

def registrar_run(exitosa, duracion_segundos, bonus_count):
    stats = cargar_stats()
    if exitosa:
        stats['runs_completadas'] += 1
    else:
        stats['runs_fallidas'] += 1
    stats['bonus_recibidos'] += bonus_count
    stats['tiempo_total_minutos'] += duracion_segundos / 60
    stats['historial'].append({
        'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'exitosa': exitosa,
        'duracion_segundos': round(duracion_segundos, 1),
        'bonus': bonus_count
    })
    if len(stats['historial']) > 500:
        stats['historial'] = stats['historial'][-500:]
    guardar_stats(stats)
    return stats