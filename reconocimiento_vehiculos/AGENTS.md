# Instrucciones para OpenCode — reconocimiento_vehiculos

## Contexto
Proyecto académico (Politécnico Internacional): sistema de reconocimiento y conteo
de vehículos con Python y OpenCV. El entregable final es un PDF que documenta
el desarrollo con capturas reales de cada etapa.

## Reglas de trabajo obligatorias
1. Trabajar por etapas. No implementar más de una etapa por vez sin confirmación.
2. NUNCA afirmar que algo funciona sin haberlo ejecutado y verificado en esta terminal.
3. Si aparece un error: mostrar el mensaje real, identificar la causa, corregir y repetir la prueba.
4. No eliminar archivos ni reinstalar componentes sin entender primero el problema.
5. No instalar bibliotecas innecesarias (TensorFlow/PyTorch solo si el modelo lo exige).
6. No inventar la procedencia del modelo ni resultados de pruebas no ejecutadas.
7. Mantener el código modular: src/detector.py, src/imagenes.py, src/videos.py.
8. Usar únicamente el entorno virtual .venv del proyecto (nunca Python global).
9. Los resultados generados van en resultados/ (imágenes y videos procesados).
10. Comandos PowerShell 5.1: usar `cmd1; if ($?) { cmd2 }` en lugar de `&&`.

## Estado del proyecto
- [x] Etapa 2: estructura de carpetas creada
- [x] Etapa 3: entorno virtual .venv
- [x] Etapa 4: opencv-python instalado, requirements.txt generado
- [x] Etapa 5: modelo cars.xml descargado y verificado (carga con empty() == False)
- [x] Etapa 6 (plan docente): src/detector.py implementado. 6/6 pruebas unitarias OK.
  Lección registrada: con XML corrupto, los bindings de OpenCV 4.14 lanzan
  cv2.error/SystemError en el constructor; se capturan ambas y se convierten
  en RuntimeError con mensaje comprensible.
- [x] Etapa 7 (plan docente): src/imagenes.py + main.py con modo imagen.
  Probado: detección real (fotograma 250 de trafico1.avi → 1 detección),
  resultado guardado con rectángulos verdes verificados, y manejo de
  errores (archivo inexistente y formato inválido, código de salida 1).
- [x] Etapa 8 (plan docente): src/videos.py + main.py con modo video.
  Probado: 10 fotogramas procesados, 9 con detecciones (17 totales),
  video de salida guardado y legible, error de video inexistente con
  código de salida 1. Pausa controlada con waitKey(pausa_ms), ESC
  para salir, liberación de recursos en bloque finally.
- [ ] Etapa 9 (plan docente): suite de pruebas y de aceptación completa
- [ ] Etapa 10 (plan docente): contenido para el informe PDF

## Modelo
- Archivo: modelos/cars.xml (Haar Cascade de vehículos)
- Fuente: https://github.com/andrewssobral/vehicle_detection_haarcascades
- Nota: el repositorio oficial de OpenCV no incluye un cascade de autos.
- El docente aún no ha confirmado un XML específico; revisar la guía de Teams
  antes de la entrega y ajustar si exige otro modelo.

## Convenciones
- Español para mensajes de usuario, docstrings y comentarios.
- Errores con mensajes comprensibles (archivos inexistentes, video no abrible, XML inválido).
- Conteo por fotograma como objetivo básico; el conteo de vehículos únicos
  (tracking) solo si la guía del docente lo exige.
- OpenCV fijado en 4.x (`opencv-python<5`): la versión 5.0 eliminó
  `CascadeClassifier` del módulo principal. No actualizar a 5.x sin revisar
  esta decisión.
