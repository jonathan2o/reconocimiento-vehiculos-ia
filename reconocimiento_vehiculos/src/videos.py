"""Procesamiento de videos: análisis fotograma a fotograma con pausa visual.

Funcionalidad (sección 6.2 del plan):
  1. Abrir un archivo de video con cv2.VideoCapture().
  2. Comprobar que el video se abra correctamente.
  3. Leer los fotogramas de forma secuencial.
  4. Detectar vehículos en cada fotograma.
  5. Dibujar rectángulos y mostrar el contador del fotograma actual.
  6. Controlar la pausa entre fotogramas con cv2.waitKey().
  7. Permitir finalizar con la tecla ESC.
  8. Liberar los recursos del video y cerrar las ventanas.
  9. Mostrar un resumen en la consola.

Nota importante (sección 6.3 del plan): el contador mostrado es el número
de detecciones POR FOTOGRAMA, no de vehículos únicos. Un mismo vehículo
puede aparecer en muchos fotogramas y contarse varias veces.
"""

import os

import cv2

# Controles de visualización.
TECLA_SALIR = 27  # ESC
VENTANA = "Deteccion de vehiculos - ESC para salir"

# Color BGR del texto del contador (verde claro).
COLOR_TEXTO = (0, 255, 0)


def procesar_video(
    ruta_video: str,
    detector,
    pausa_ms: int = 100,
    guardar_ruta: str | None = None,
    maximo_fotogramas: int | None = None,
) -> dict:
    """Procesa un video fotograma a fotograma mostrando las detecciones.

    - pausa_ms: milisegundos de espera entre fotogramas. Controla la
      VELOCIDAD DE REPRODUCCIÓN (observación), no la velocidad de
      procesamiento. Con pausa_ms=100 se muestra ~1 fotograma cada
      100 ms (unos 10 por segundo), muy ralentizado para observar.
    - guardar_ruta: si se indica, guarda el video procesado.
    - maximo_fotogramas: límite opcional de fotogramas a procesar
      (útil para pruebas; None procesa todo el video).

    Devuelve un diccionario con estadísticas del procesamiento.
    Lanza FileNotFoundError si el archivo no existe y ValueError si
    el video no puede abrirse.
    """
    if not os.path.isfile(ruta_video):
        raise FileNotFoundError(
            f"No se encontró el video en la ruta: '{ruta_video}'. "
            "Coloca el archivo en 'datos/videos/' o indica otra ruta."
        )

    captura = cv2.VideoCapture(ruta_video)
    if not captura.isOpened():
        raise ValueError(
            f"OpenCV no pudo abrir el video '{ruta_video}'. "
            "Verifica que el archivo sea un video válido y no esté dañado."
        )

    ancho = int(captura.get(cv2.CAP_PROP_FRAME_WIDTH))
    alto = int(captura.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps_origen = captura.get(cv2.CAP_PROP_FPS) or 15.0
    total = int(captura.get(cv2.CAP_PROP_FRAME_COUNT))

    escritor = None
    if guardar_ruta:
        os.makedirs(os.path.dirname(guardar_ruta), exist_ok=True)
        cuatrocc = cv2.VideoWriter_fourcc(*"MJPG")
        escritor = cv2.VideoWriter(guardar_ruta, cuatrocc, fps_origen, (ancho, alto))

    print(f"Video: {os.path.basename(ruta_video)} ({total} fotogramas, {fps_origen:.1f} FPS)")
    print(f"Pausa de visualización: {pausa_ms} ms entre fotogramas (ESC para salir)")

    estadisticas = {
        "fotogramas_procesados": 0,
        "fotogramas_con_detecciones": 0,
        "total_detecciones": 0,
        "completado": False,
    }
    interrumpido_por_usuario = False

    try:
        while True:
            leido, fotograma = captura.read()
            if not leido:
                break  # Fin del video.

            rectangulos, _ = detector.detectar(fotograma)
            resultado = detector.dibujar(fotograma, rectangulos)

            # Contador del fotograma actual, dibujado sobre la imagen.
            texto = f"Fotograma {estadisticas['fotogramas_procesados'] + 1} | Detecciones: {len(rectangulos)}"
            cv2.putText(
                resultado, texto, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, COLOR_TEXTO, 2,
            )

            cv2.imshow(VENTANA, resultado)
            if escritor is not None:
                escritor.write(resultado)

            estadisticas["fotogramas_procesados"] += 1
            if len(rectangulos) > 0:
                estadisticas["fotogramas_con_detecciones"] += 1
                estadisticas["total_detecciones"] += len(rectangulos)

            # waitKey controla la pausa de reproducción; devuelve -1 si
            # no se pulsó ninguna tecla en el intervalo indicado.
            if cv2.waitKey(pausa_ms) & 0xFF == TECLA_SALIR:
                interrumpido_por_usuario = True
                print("Reproducción finalizada por el usuario (ESC).")
                break

            if (
                maximo_fotogramas is not None
                and estadisticas["fotogramas_procesados"] >= maximo_fotogramas
            ):
                break

        estadisticas["completado"] = not interrumpido_por_usuario
    finally:
        # Liberación de recursos SIEMPRE, incluso si hay una excepción.
        captura.release()
        if escritor is not None:
            escritor.release()
        cv2.destroyAllWindows()

    if estadisticas["completado"]:
        print("Procesamiento del video completado hasta el final.")
    print(f"Fotogramas procesados: {estadisticas['fotogramas_procesados']}")
    print(f"Fotogramas con detecciones: {estadisticas['fotogramas_con_detecciones']}")
    print(f"Total de detecciones (por fotograma): {estadisticas['total_detecciones']}")

    if escritor is not None and guardar_ruta:
        print(f"Video procesado guardado en: {guardar_ruta}")

    return estadisticas
