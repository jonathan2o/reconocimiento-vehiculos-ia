"""Pruebas automatizadas del detector (biblioteca estándar unittest).

Casos cubiertos (criterios de aceptación 3 y 4 del proyecto):
  1. El modelo válido (modelos/cars.xml) se carga.
  2. Una ruta inexistente produce un error comprensible.
  3. Un XML corrupto produce un error comprensible.
  4. detectar() falla con un fotograma inválido (sanidad).
  5. dibujar() dibuja los rectángulos sin alterar el original.
"""

import os
import tempfile
import unittest

import cv2
import numpy as np

from src.detector import DetectorVehiculos

RUTA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_MODELO = os.path.join(RUTA_PROYECTO, "modelos", "cars.xml")


class TestCargaModelo(unittest.TestCase):
    """Criterio 3: el modelo válido se carga."""

    def test_modelo_valido_se_carga(self):
        detector = DetectorVehiculos(RUTA_MODELO)
        self.assertFalse(detector._clasificador.empty())

    def test_modelo_inexistente_lanza_error(self):
        with self.assertRaises(FileNotFoundError) as contexto:
            DetectorVehiculos("modelos/no_existe.xml")
        self.assertIn("No se encontró el modelo", str(contexto.exception))

class TestModeloInvalido(unittest.TestCase):
    """Criterio 4: un modelo incompatible produce un error comprensible."""

    def test_xml_corrupto_lanza_error(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = os.path.join(carpeta, "corrupto.xml")
            with open(ruta, "w", encoding="utf-8") as archivo:
                archivo.write("esto no es un clasificador haar")
            with self.assertRaises(RuntimeError) as contexto:
                DetectorVehiculos(ruta)
            self.assertIn("no es un clasificador Haar", str(contexto.exception))


class TestDeteccion(unittest.TestCase):
    """Sanidad de detectar() y dibujar() con fotogramas controlados."""

    def setUp(self):
        self.detector = DetectorVehiculos(RUTA_MODELO)
        # Fotograma negro de 240x320 (alto, ancho) sin contenido.
        self.fotograma = np.zeros((240, 320, 3), dtype=np.uint8)

    def test_fotograma_invalido_lanza_error(self):
        with self.assertRaises(ValueError):
            self.detector.detectar(None)

    def test_fotograma_vacio_devuelve_lista(self):
        rectangulos, _ = self.detector.detectar(self.fotograma)
        self.assertIsInstance(rectangulos, list)

    def test_dibujar_modifica_copia(self):
        original = self.fotograma.copy()
        rectangulos = [(10, 10, 50, 50)]
        resultado = self.detector.dibujar(self.fotograma, rectangulos)
        self.assertEqual(resultado.shape, self.fotograma.shape)
        # El fotograma original no debe alterarse.
        np.testing.assert_array_equal(self.fotograma, original)
        # El resultado debe diferir en la zona del rectángulo.
        self.assertFalse(np.array_equal(resultado, self.fotograma))


if __name__ == "__main__":
    unittest.main()
