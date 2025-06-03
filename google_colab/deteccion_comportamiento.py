import cv2
import time
import numpy as np
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
from collections import defaultdict

# Cargar modelo
model = YOLO("yolov8x.pt")

# Inicializar tracker DeepSORT
tracker = DeepSort(max_age=30)

# Historial de posiciones por ID
position_history = defaultdict(list)
stationary_start_time = {}

# Parámetros
PIXEL_TOLERANCE = 25  # tolerancia para considerar inmóvil
TIME_THRESHOLD = 10   # segundos para marcar sospechoso

# Cargar video fuente
cap = cv2.VideoCapture("deteccion_comportamiento.mp4")

# Obtener propiedades para guardar video
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_monitoreo.mp4', fourcc, fps, (width, height))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]
    detections = []

    for box in results.boxes.data:
        x1, y1, x2, y2, conf, cls = box
        if int(cls) == 0:
            detections.append(([int(x1), int(y1), int(x2 - x1), int(y2 - y1)], conf, 'person'))

    tracks = tracker.update_tracks(detections, frame=frame)

    current_time = time.time()
    for track in tracks:
        if not track.is_confirmed():
            continue
        track_id = track.track_id
        l, t, r, b = track.to_ltrb()
        cx = int((l + r) / 2)
        cy = int((t + b) / 2)

        position_history[track_id].append((cx, cy, current_time))

        if len(position_history[track_id]) > 100:
            position_history[track_id] = position_history[track_id][-100:]

        history = position_history[track_id]
        if len(history) > 2:
            initial_pos = history[0][:2]
            if all(np.linalg.norm(np.array(initial_pos) - np.array(pos[:2])) < PIXEL_TOLERANCE for pos in history):
                if track_id not in stationary_start_time:
                    stationary_start_time[track_id] = history[0][2]
                else:
                    duration = current_time - stationary_start_time[track_id]
                    if duration > TIME_THRESHOLD:
                        label = f'🚨 ID {track_id} sospechoso ({int(duration)}s)'
                        color = (0, 0, 255)
                        cv2.putText(frame, label, (cx - 50, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                        cv2.rectangle(frame, (int(l), int(t)), (int(r), int(b)), color, 2)
                        continue
            else:
                stationary_start_time.pop(track_id, None)

        # # Dibujar tracking normal
        # cv2.rectangle(frame, (int(l), int(t)), (int(r), int(b)), (0, 255, 0), 2)
        # cv2.putText(frame, f'ID {track_id}', (cx - 20, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

    # Guardar frame procesado en archivo de salida
    out.write(frame)

cap.release()
out.release()

print("Video procesado y guardado como 'output_monitoreo.mp4'")

# Para descargar en Colab:
from google.colab import files
files.download('output_monitoreo.mp4')
