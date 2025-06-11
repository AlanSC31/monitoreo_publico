# Monitoreo espacios públicos

## Descripción
### Pendiente

## Get started

Los scripts se pueden correr de dos maneras: de forma local, viendo en tiempo real el procesamiento del *source* (lo cual consume muchos recursos), y en la nube, utilizando *Google Colab*.

### Local.
#### Requisitos:
1. Descargar el modelo yolo 8x: [Aqui](https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8m.pt) y colocarlo en una carpeta llamada `models` en la raiz del proyecto.
2. Python 3.13.3^.
3. Librerías de Python: *ultralytics* y *deep_sort_realtime*.

#### Instalación y ejecución.
1. Instalar Python.
2. Instalar las librerías mencionadas con: `pip install ultralytics` y `pip install deep_sort_realtime`
3. Navegar en la terminal hasta la carpeta raíz del proyecto y ejecutar el script con: `python [nombre del archivo]`

### Google Colab.
#### Instalación y ejecución.
1. Abrir una sesión de Google Colab.
2. Descargar el modelo yolo 8x: [Aqui](https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8x.pt)
2. Subir el proyecto y el modelo al notebook de Google Colab todos los archivos en la raiz.
3. Instalar las librerías necesarias: `pip install ultralytics`, `pip install deep_sort_realtime`.
4. Ejecutar los scripts con: `!python [nombre del archivo]`

Esto generará el *output* en la carpeta raíz.

https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8m.pt

