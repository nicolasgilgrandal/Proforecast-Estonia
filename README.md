# Proforecast-Estonia
Este proyecto desarrolla un modelo de Machine Learning para predecir el consumo y producción energética de prosumidores en Estonia. Se lleva a cabo una limpieza de los datos y una creación de nuevas variables para mejorar las predicciones. Ideal para gestores energéticos y análisis de autosuficiencia energética para distintos tipos de usuarios. 

# Descripción General
Con la creciente demanda de energías renovables y optimización de la eficiencia energética, este modelo ofrece una herramienta crucial para predecir la producción y consumo energético, mejorando la planificación energética en de la compañía Eesti Energia.




# Proyecto de Predicción de Consumo y Producción Energética en Prosumidores de Estonia
## Visión General del Proyecto
### Motivación
**Proforecast Estonia** proyecto nace de la necesidad de optimizar la gestión de la energía en un determinado número de clientes de la empresa Eesti Energia distribuidos a lo largo de la geografía de Estonia.   Estos clientes cuentan con la peculiaridad de ser prosumidoes, esto es, no solo consumidores de energía sino tambien productores mediante instalaciones fotovoltaicas. El objetivo radica en aplicar modelos estadísticos avanzados para predecir el consumo y la producción energética, con potencial para adaptar el modelo para predicciones en tiempo real durante fluctuaciones diarias o estacionales.

### Fuente de Datos
Los datos para este proyecto son proporcionados íntegramente por Eesti Energy. La compañía ha facilitado acceso a los siguientes conjuntos de datos a través de la plataforma Kaggle:

* Consumo y Producción Energética: Datos detallados sobre el consumo y producción de energía por hora para prosumidores en Estonia.
* Información Meteorológica: Datos sobre las condiciones climáticas que influyen directamente en la producción de energía solar.




## Detalles de los Datos
### Datos Brutos
Los datos de consumo y producción energética se recopilan de forma continua, registrando mediciones cada hora, lo que resulta en 24 lecturas diarias por usuario. Cada registro especifica la cantidad de energía consumida o producida, medida en kilovatios-hora (kWh). Estos datos son recabados para cada prosumidor, permitiendo un seguimiento detallado y personalizado del flujo energético.

#### Diversidad de Prosumidores
Los datos abarcan dos categorías principales de prosumidores: empresas y particulares. Dentro de estas categorías, existen cuatro tipos de contratos entre los prosumidores y la compañía Eesti Energy, cada uno con condiciones específicas que podrían influir en los patrones de consumo y producción. Esta diversidad en los tipos de contratos y prosumidores enriquece el análisis, permitiendo ajustes y predicciones más precisas según las características contractuales y el tipo de usuario.
