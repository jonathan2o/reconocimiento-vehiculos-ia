"""Punto de entrada del sistema de reconocimiento y conteo de vehículos.

Proyecto académico - Politécnico Internacional.

Modos disponibles:
  - imagen: analiza una fotografía de tráfico y guarda el resultado.
  - video:  analiza un video fotograma a fotograma (Etapa 7).
"""

import argparse
import os
import sys

from src.detector import DetectorVehiculos
from src.imagenes import procesar_imagen
from src.videos import procesar_video

RUTA_MODELO = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "modelos", "cars.xml"
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Reconocimiento y conteo de vehículos con OpenCV."
    )
    parser.add_argument(
        "modo",
        choices=["imagen", "video"],
        help="Tipo de archivo a analizar.",
    )
    parser.add_argument(
        "ruta",
        help="Ruta del archivo (imagen o video) a procesar.",
    )
    parser.add_argument(
        "--pausa",
        type=int,
        default=100,
        help="Milisegundos de pausa entre fotogramas del video (default: 100).",
    )
    parser.add_argument(
        "--guardar-video",
        action="store_true",
        help="Guardar el video procesado en resultados/videos/.",
    )
    argumentos = parser.parse_args()

    if not os.path.isfile(argumentos.ruta):
        print(f"Error: no existe el archivo '{argumentos.ruta}'.")
        return 1

    try:
        detector = DetectorVehiculos(RUTA_MODELO)
    except (FileNotFoundError, RuntimeError) as error:
        print(f"Error al cargar el modelo: {error}")
        return 1

    if argumentos.modo == "imagen":
        try:
            procesar_imagen(argumentos.ruta, detector)
        except (FileNotFoundError, ValueError) as error:
            print(f"Error al procesar la imagen: {error}")
            return 1
        return 0

    if argumentos.modo == "video":
        ruta_salida = None
        if argumentos.guardar_video:
            nombre = os.path.splitext(os.path.basename(argumentos.ruta))[0]
            base = os.path.dirname(os.path.abspath(__file__))
            ruta_salida = os.path.join(base, "resultados", "videos", f"{nombre}_procesado.avi")
        try:
            procesar_video(argumentos.ruta, detector, pausa_ms=argumentos.pausa, guardar_ruta=ruta_salida)
        except (FileNotFoundError, ValueError) as error:
            print(f"Error al procesar el video: {error}")
            return 1
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
