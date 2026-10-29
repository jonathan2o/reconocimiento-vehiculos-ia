"""Procesamiento de imágenes: detección, conteo y guardado de resultados.

Funcionalidad (sección 6.1 del plan):
  1. Recibir la ruta de una imagen.
  2. Comprobar que el archivo existe.
  3. Cargar la imagen con OpenCV.
  4. Verificar que se haya leído correctamente.
  5. Ejecutar el detector.
  6. Dibujar rectángulos sobre los vehículos detectados.
  7. Mostrar el número de detecciones.
  8. Guardar la imagen procesada en resultados/imagenes/.
"""

import os

import cv2


def procesar_imagen(
    ruta_imagen: str,
    detector,
    mostrar: bool = True,
    guardar: bool = True,
) -> int:
    """Analiza una imagen, dibuja detecciones y guarda el resultado.

    Devuelve el número de detecciones obtenidas. Lanza FileNotFoundError
    si la ruta no existe y ValueError si la imagen no puede leerse.
    """
    if not os.path.isfile(ruta_imagen):
        raise FileNotFoundError(
            f"No se encontró la imagen en la ruta: '{ruta_imagen}'. "
            "Coloca el archivo en 'datos/imagenes/' o indica otra ruta."
        )

    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        raise ValueError(
            f"OpenCV no pudo leer la imagen '{ruta_imagen}'. "
            "Verifica que sea un formato compatible (jpg, png, bmp)."
        )

    rectangulos, _ = detector.detectar(imagen)
    resultado = detector.dibujar(imagen, rectangulos)

    print(f"Imagen analizada: {os.path.basename(ruta_imagen)}")
    print(f"Detecciones obtenidas: {len(rectangulos)}")

    if mostrar:
        cv2.imshow("Deteccion de vehiculos (tecla ESC para cerrar)", resultado)
        while True:
            tecla = cv2.waitKey(30) & 0xFF
            if tecla == 27:  # ESC
                break
        cv2.destroyAllWindows()

    if guardar:
        carpeta_destino = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "resultados",
            "imagenes",
        )
        os.makedirs(carpeta_destino, exist_ok=True)
        nombre, extension = os.path.splitext(os.path.basename(ruta_imagen))
        ruta_salida = os.path.join(carpeta_destino, f"{nombre}_procesada{extension}")
        correcto = cv2.imwrite(ruta_salida, resultado)
        if correcto:
            print(f"Resultado guardado correctamente en: {ruta_salida}")
        else:
            print(f"Advertencia: no se pudo guardar el resultado en '{ruta_salida}'.")

    return len(rectangulos)
