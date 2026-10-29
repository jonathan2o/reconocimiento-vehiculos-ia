# Fuente del modelo

## Archivo
`cars.xml` — clasificador Haar Cascade entrenado para detección de vehículos.
Tamaño: 118 803 bytes. Verificado: se carga con `cv2.CascadeClassifier` y
`empty()` devuelve `False` (OpenCV 4.14.0, Python 3.13, Windows).

## Procedencia
- Repositorio: <https://github.com/andrewssobral/vehicle_detection_haarcascades>
  ("Vehicle Detection by Haar Cascades with OpenCV", 559 estrellas, 509 forks)
- Descarga directa:
  <https://raw.githubusercontent.com/andrewssobral/vehicle_detection_haarcascades/master/cars.xml>
- Ejemplos de uso académico con este mismo archivo:
  <https://github.com/amberitas17/Car-Detection-and-Vehicle-Detection-using-OpenCV>

## Notas
- El repositorio oficial de OpenCV (`opencv/data/haarcascades`) no incluye un
  cascade de automóviles; solo rostros, ojos, cuerpos, placas rusas, etc.
- El archivo incluye el comentario interno `<!-- Add more negative to training. -->`,
  señal de que es un modelo comunitario sin documentación formal de entrenamiento.
  Por eso se documentan falsos positivos/omisiones en las pruebas (Etapa 9).
- Versión de OpenCV fijada en la línea 4.x (`opencv-python<5`): OpenCV 5.0
  eliminó `CascadeClassifier` del módulo principal, y el enfoque de la actividad
  requiere cargar XML de Haar.

## Pendiente
- Si la guía del docente (Microsoft Teams) especifica otro XML o arquitectura,
  reemplazar este modelo y actualizar este documento con la nueva fuente.
