"""Detector de vehículos mediante clasificador Haar Cascade de OpenCV.

Módulo responsable de:
  - Cargar el clasificador XML con validación de errores.
  - Detectar vehículos en un fotograma (imagen BGR).
  - Dibujar los rectángulos de las detecciones.

Nota sobre el conteo: detectar() devuelve el número de detecciones del
fotograma analizado. NO cuenta vehículos únicos: un mismo vehículo puede
aparecer en muchos fotogramas y contarse varias veces. El conteo de
vehículos únicos requeriría seguimiento de objetos (tracking), que solo
se implementará si la guía del docente lo exige.
"""

import os

import cv2

# Parámetros por defecto de detectMultiScale.
# scaleFactor: reducción de la imagen en cada pasada (más bajo = más
# detecciones pero más lento). minNeighbors: detecciones vecinas mínimas
# para aceptar un rectángulo (más alto = menos falsos positivos).
# minSize: tamaño mínimo en píxeles de un vehículo aceptable.
PARAMETROS_DEFECTO = {
    "scaleFactor": 1.05,
    "minNeighbors": 3,
    "minSize": (30, 30),
}

# Color BGR de los rectángulos (verde) y grosor del trazo.
COLOR_RECTANGULO = (0, 255, 0)
GROSOR_RECTANGULO = 2


class DetectorVehiculos:
    """Envuelve a cv2.CascadeClassifier para detectar vehículos."""

    def __init__(self, ruta_modelo: str, parametros: dict | None = None):
        """Carga el clasificador XML indicado.

        Lanza FileNotFoundError si el archivo no existe y RuntimeError si
        OpenCV no puede interpretarlo como clasificador Haar válido.
        """
        if not os.path.isfile(ruta_modelo):
            raise FileNotFoundError(
                f"No se encontró el modelo en la ruta: '{ruta_modelo}'. "
                "Verifica que el archivo XML exista en la carpeta 'modelos'."
            )

        try:
            self._clasificador = cv2.CascadeClassifier(ruta_modelo)
        except (cv2.error, SystemError) as error:
            raise RuntimeError(
                f"El archivo '{ruta_modelo}' no es un clasificador Haar "
                "válido o está dañado. Verifica su procedencia y formato."
            ) from error

        if self._clasificador is None or self._clasificador.empty():
            raise RuntimeError(
                f"El archivo '{ruta_modelo}' no es un clasificador Haar "
                "válido o está dañado. Verifica su procedencia y formato."
            )

        self._parametros = dict(PARAMETROS_DEFECTO)
        if parametros:
            self._parametros.update(parametros)

    @property
    def parametros(self) -> dict:
        """Parámetros vigentes de detectMultiScale."""
        return dict(self._parametros)

    def detectar(self, fotograma):
        """Detecta vehículos en un fotograma.

        Recibe una imagen BGR (como las entregadas por cv2.imread o
        VideoCapture.read) y devuelve una lista de rectángulos
        (x, y, ancho, alto) y la versión en escala de grises usada.
        """
        if fotograma is None:
            raise ValueError(
                "No se recibió un fotograma válido para analizar."
            )

        gris = cv2.cvtColor(fotograma, cv2.COLOR_BGR2GRAY)
        gris = cv2.equalizeHist(gris)

        rectangulos = self._clasificador.detectMultiScale(
            gris,
            scaleFactor=self._parametros["scaleFactor"],
            minNeighbors=self._parametros["minNeighbors"],
            minSize=self._parametros["minSize"],
        )

        # detectMultiScale devuelve un ndarray vacío si no hay coincidencias.
        if rectangulos is None or len(rectangulos) == 0:
            return [], gris
        return [tuple(int(v) for v in r) for r in rectangulos], gris

    def dibujar(self, fotograma, rectangulos):
        """Dibuja un rectángulo verde sobre cada detección.

        Trabaja sobre una copia para no alterar el fotograma original.
        """
        resultado = fotograma.copy()
        for x, y, ancho, alto in rectangulos:
            cv2.rectangle(
                resultado,
                (x, y),
                (x + ancho, y + alto),
                COLOR_RECTANGULO,
                GROSOR_RECTANGULO,
            )
        return resultado
