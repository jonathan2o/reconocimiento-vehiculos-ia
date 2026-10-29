# Sistema de reconocimiento y conteo de vehículos (Python + OpenCV)

Proyecto académico — Politécnico Internacional.

Analiza imágenes y videos de tráfico para detectar vehículos mediante un
clasificador Haar Cascade (XML) cargado con OpenCV, dibuja rectángulos sobre
las detecciones y muestra un contador.

## Estructura

```
reconocimiento_vehiculos/
├── .venv/                  Entorno virtual de Python
├── modelos/                Modelo XML (cars.xml) y su documentación de fuente
├── datos/
│   ├── imagenes/           Fotografías de entrada
│   └── videos/             Videos de entrada
├── resultados/
│   ├── imagenes/           Imágenes procesadas (evidencias)
│   └── videos/             Videos procesados (evidencias)
├── src/                    Código fuente (detector, imágenes, videos)
├── tests/                  Pruebas automatizadas (unittest)
├── main.py                 Punto de entrada
├── requirements.txt        Dependencias
└── AGENTS.md               Instrucciones de trabajo
```

## Configuración (Windows, PowerShell)

```powershell
cd reconocimiento_vehiculos
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

> Importante: `requirements.txt` fija `opencv-python` en la línea 4.x.
> OpenCV 5.0 eliminó `CascadeClassifier`, necesario para cargar el XML de Haar.

## Ejecución

```powershell
# Analizar una imagen (cierra la ventana con ESC)
python main.py imagen datos\imagenes\trafico1.jpg

# Analizar un video (pausa de 100 ms entre fotogramas por defecto)
python main.py video datos\videos\trafico1.avi

# Video más lento (200 ms/fotograma) y guardando el resultado
python main.py video datos\videos\trafico1.avi --pausa 200 --guardar-video
```

En modo imagen se guarda `resultados/imagenes/<nombre>_procesada.jpg`.
Con `--guardar-video` se guarda `resultados/videos/<nombre>_procesado.avi`.

> La pausa (`--pausa`) controla la **velocidad de reproducción** para poder
> observar las detecciones; no debe confundirse con la velocidad de
> **procesamiento** (cuántos fotogramas analiza el programa por segundo).

## Modelo utilizado

- Archivo: `modelos/cars.xml` (Haar Cascade de vehículos)
- Fuente: <https://github.com/andrewssobral/vehicle_detection_haarcascades>
- Detalle y licencia: ver `modelos/FUENTE_MODELO.md`

El repositorio oficial de OpenCV (`opencv/data/haarcascades`) no incluye un
cascade de automóviles, por lo que se emplea un modelo comunitario documentado.

## Limitaciones conocidas

- Un Haar Cascade puede producir falsos positivos y omisiones según la
  iluminación, el ángulo de la cámara y la calidad de la imagen.
- El contador inicial es **por fotograma**: un mismo vehículo puede aparecer
  en muchos fotogramas y contarse varias veces. El conteo de vehículos únicos
  (tracking) se evaluará solo si la guía lo exige.

## Estado

- [x] Estructura del proyecto
- [x] Entorno virtual y dependencias
- [x] Modelo descargado y verificado
- [ ] Detector (`src/detector.py`)
- [ ] Procesamiento de imágenes (`src/imagenes.py`)
- [ ] Procesamiento de videos (`src/videos.py`)
- [ ] Pruebas automatizadas
