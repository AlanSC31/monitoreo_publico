from ultralytics import YOLO
import cv2
import numpy as np
import time
from google.colab.patches import cv2_imshow  # solo para debug, no necesario

# Cargar modelo
model = YOLO("yolov8x.pt")

# Cargar source
cap = cv2.VideoCapture("personas_calle_3.mp4")

# Configuración del writer para guardar video procesado
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('conteo_area.mp4', fourcc, fps, (width, height))

# Grid y configuración
grid_size = (2, 2)
umbral_concurrido = 5
persona_tiempos = {}
persona_celdas = {}
last_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time

    cell_height = height // grid_size[0]
    cell_width = width // grid_size[1]

    results = model.track(source=frame, persist=True, conf=0.4, classes=[0], tracker='bytetrack.yaml', verbose=False)
    grid_counts = np.zeros(grid_size, dtype=int)

    if results and results[0].boxes.id is not None:
        ids = results[0].boxes.id.int().tolist()
        for i, box in enumerate(results[0].boxes.xyxy):
            id_persona = ids[i]
            x1, y1, x2, y2 = map(int, box)

            cell_x = min(width - 1, x1) // cell_width
            cell_y = min(height - 1, y1) // cell_height
            celda_actual = (cell_y, cell_x)

            grid_counts[cell_y, cell_x] += 1

            if id_persona not in persona_tiempos:
                persona_tiempos[id_persona] = {}
                persona_celdas[id_persona] = celda_actual

            celda_anterior = persona_celdas.get(id_persona)
            if celda_actual == celda_anterior:
                persona_tiempos[id_persona][celda_actual] = persona_tiempos[id_persona].get(celda_actual, 0) + delta_time
            else:
                persona_celdas[id_persona] = celda_actual
                if celda_actual not in persona_tiempos[id_persona]:
                    persona_tiempos[id_persona][celda_actual] = 0

            tiempo = persona_tiempos[id_persona][celda_actual]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            cv2.putText(frame, f"ID:{id_persona} T:{int(tiempo)}s", (cx, cy - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            x1, y1 = j * cell_width, i * cell_height
            x2, y2 = (j + 1) * cell_width, (i + 1) * cell_height
            color = (0, 0, 255) if grid_counts[i, j] >= umbral_concurrido else (0, 255, 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, f"{grid_counts[i,j]} p", (x1 + 5, y1 + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    out.write(frame)  # Guardar frame en video

cap.release()
out.release()
