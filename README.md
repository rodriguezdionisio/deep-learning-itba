# Deep Learning ITBA

### Problemática: 
Optimización de la producción de un restaurante.
Una mala planificación de la producción en un restaurante puede causar desperdicio de alimentos, aumento de costos operativos y, por ende, disminuir la rentabilidad. También lleva a falta de stock para satisfacer al cliente, o a demoras en el servicio e inconsistencia en la calidad de los platos por tener a los cocineros afectados a la producción en horarios pico de demanda. A esto se le puede agregar el malestar en los empleados producto de la falta de organización y el mal uso de su tiempo.

### Solución propuesta: 
Se buscará organizar y optimizar la producción de un restaurante mediante un modelo de optimización, en base a la predicción de demanda semanal de productos.

### Desarrollo:
Se partirá de un dataset de “adiciones” obtenido al conectarse a la API de Fudo, un software de gestión gastronómica. El dataset consiste en el detalle (o adiciones) de productos añadidos en cada mesa (venta).
Este dataset será procesado para obtener la venta diaria de productos.
Se realizará un pronóstico de la demanda de productos para la próxima semana utilizando un modelo de Deep Learning pre entrenado basado en transformers (Temporal Fusion Transformers o TFT). 
Con los datos de la demanda se procederá a alimentar un modelo de optimización de producción basado en un algoritmo de programación entera. Esto será posible gracias a las librerías PuLP o Pyomo de Python.
Estos modelos de programación permitirán modelar un problema de optimización de la producción considerando múltiples restricciones como la demanda pronosticada, la receta de cada producto, el tiempo de preparación y el tamaño del lote, la disponibilidad de horas de trabajo de los cocineros, y otras restricciones relevantes.

### Repositorio
El repositorio consiste en cinco notebooks principales:
- 1_fetch_data: se obtiene la información de ventas del transaccional
- 1_fetch_clima: se obtiene y procesa la información del clima
- 2_process_sales: se limpia y procesa la información de ventas
- 3_prediction_tft_model: se prepara el dataset para las predicciones y se entrena el modelo TFT y baseline
- 4_predictions: se generan las predicciones de ventas futuras

Actualmente trabajando en el código de optimización de la producción.

Además hay otros archivos con funciones necesarias para interactuar con las APIs de Google Drive, Fudo y holidays.
