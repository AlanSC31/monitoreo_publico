import cv2
import time
import numpy as np
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
from collections import defaultdict

# Cargar modelo 
model = YOLO("yolov8n.pt") 

# Inicializar el tracker DeepSORT
tracker = DeepSort(max_age=30)

# Historial de posiciones por ID
position_history = defaultdict(list)
stationary_start_time = {}

# Parámetros
PIXEL_TOLERANCE = 25  # tolerancia en desplazamiento para considerar que sigue en el mismo lugar
TIME_THRESHOLD = 10   # segundos que debe estar inmóvil para marcar como sospechoso

# Cargar source
cap = cv2.VideoCapture("src/videos/personas_calle_3.mp4")  # o ruta a archivo .mp4

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]
    detections = []

    for box in results.boxes.data:
        x1, y1, x2, y2, conf, cls = box
        if int(cls) == 0:  # solo clase "person"
            detections.append(([int(x1), int(y1), int(x2 - x1), int(y2 - y1)], conf, 'person'))

    tracks = tracker.update_tracks(detections, frame=frame)

    current_time = time.time()
    for track in tracks:
        if not track.is_confirmed():
            continue
        track_id = track.track_id
        l, t, w, h = track.to_ltrb()
        cx = int((l + w) / 2)
        cy = int((t + h) / 2)

        position_history[track_id].append((cx, cy, current_time))

        # Limitar historial (para evitar memoria infinita)
        if len(position_history[track_id]) > 100:
            position_history[track_id] = position_history[track_id][-100:]

        # Calcular si la persona esta quieta
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
                        cv2.rectangle(frame, (int(l), int(t)), (int(w), int(h)), color, 2)
                        continue
            else:
                stationary_start_time.pop(track_id, None)

        # # Dibujar tracking normal
        # cv2.rectangle(frame, (int(l), int(t)), (int(w), int(h)), (0, 255, 0), 2)
        # cv2.putText(frame, f'ID {track_id}', (cx - 20, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

    cv2.imshow("Monitoreo", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()