from ultralytics import YOLO
import cv2
import numpy as np
import time

# Cargar modelo
model = YOLO("yolov8m.pt")

# Cargar source
cap = cv2.VideoCapture("src/videos/personas_calle_3.mp4")

# Configuracion del grid
grid_size = (2, 2)
umbral_concurrido = 5

# Historial de tiempo por persona y celda
persona_tiempos = {}  # {id: {(celda_y, celda_x): tiempo}}
persona_celdas = {}   # {id: (celda_y, celda_x)}

last_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Calcular delta de tiempo
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time

    # Dividir el frame en celdas
    height, width, _ = frame.shape
    cell_height = height // grid_size[0]
    cell_width = width // grid_size[1]

    # Ejecutar tracking
    results = model.track(source=frame, persist=True, conf=0.3, classes=[0], verbose=False)

    # Inicializar conteo por celda
    grid_counts = np.zeros(grid_size, dtype=int)

    if results and results[0].boxes.id is not None:
        ids = results[0].boxes.id.int().tolist()
        for i, box in enumerate(results[0].boxes.xyxy):
            id_persona = ids[i]
            x1, y1, x2, y2 = map(int, box)

            # Calcular celda actual
            cell_x = min(width - 1, x1) // cell_width
            cell_y = min(height - 1, y1) // cell_height
            celda_actual = (cell_y, cell_x)

            # Aumentar contador por celda
            grid_counts[cell_y, cell_x] += 1

            # Inicializar si es nuevo
            if id_persona not in persona_tiempos:
                persona_tiempos[id_persona] = {}
                persona_celdas[id_persona] = celda_actual

            # Obtener celda anterior
            celda_anterior = persona_celdas.get(id_persona)

            # Si sigue en la misma celda, acumular tiempo
            if celda_actual == celda_anterior:
                persona_tiempos[id_persona][celda_actual] = persona_tiempos[id_persona].get(celda_actual, 0) + delta_time
            else:
                # Si cambio de celda, actualizar su posición
                persona_celdas[id_persona] = celda_actual
                # Iniciar tiempo si no existia
                if celda_actual not in persona_tiempos[id_persona]:
                    persona_tiempos[id_persona][celda_actual] = 0

            # Mostrar tiempo acumulado en esa celda para esa persona
            tiempo = persona_tiempos[id_persona][celda_actual]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            cv2.putText(frame, f"ID:{id_persona} T:{int(tiempo)}s", (cx, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

    # Dibujar grid y cantidad de personas
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            x1, y1 = j * cell_width, i * cell_height
            x2, y2 = (j + 1) * cell_width, (i + 1) * cell_height
            color = (0, 0, 255) if grid_counts[i, j] >= umbral_concurrido else (0, 255, 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, f"{grid_counts[i,j]} p", (x1 + 5, y1 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cv2.imshow("Conteo y tiempo por persona en areas", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
