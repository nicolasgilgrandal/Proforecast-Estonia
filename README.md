# Proforecast-Estonia
Este proyecto desarrolla un modelo de Machine Learning para predecir el consumo y producción energética de prosumidores en Estonia. Se lleva a cabo una limpieza de los datos y una creación de nuevas variables para mejorar las predicciones. Ideal para gestores energéticos y análisis de autosuficiencia energética para distintos tipos de usuarios. 

# Descripción General
Con la creciente demanda de energías renovables y optimización de la eficiencia energética, este modelo ofrece una herramienta crucial para predecir la producción y consumo energético, mejorando la planificación energética en de la compañía Eesti Energia.




# Proyecto de Predicción de Consumo y Producción Energética en Prosumidores de Estonia
## Visión General del Proyecto
### Motivación
**Proforecast Estonia** es un proyecto que nace de la necesidad de optimizar la gestión de la energía en un determinado número de clientes de la empresa Eesti Energia distribuidos a lo largo de la geografía de Estonia. Estos clientes cuentan con la peculiaridad de ser prosumidoes, esto es, no solo consumidores de energía sino tambien productores mediante instalaciones fotovoltaicas. El objetivo radica en aplicar modelos estadísticos avanzados para predecir el consumo y la producción energética, con potencial para adaptar el modelo para predicciones en tiempo real durante fluctuaciones diarias o estacionales.

### Fuente de Datos
Los datos para este proyecto son proporcionados íntegramente por Eesti Energia. La compañía ha facilitado acceso a los siguientes conjuntos de datos a través de la plataforma Kaggle:

* Consumo y Producción Energética: Datos detallados sobre el consumo y producción de energía por hora para prosumidores en Estonia.
* Información Meteorológica: Datos sobre las condiciones climáticas que influyen directamente en la producción de energía solar.

## Detalles de los Datos
### Datos Brutos
Los datos de consumo y producción energética se recopilan de forma continua, registrando mediciones cada hora, lo que resulta en 24 lecturas diarias por usuario. Cada registro especifica la cantidad de energía consumida o producida, medida en kilovatios-hora (kWh). Estos datos son recabados para cada prosumidor, permitiendo un seguimiento detallado y personalizado del flujo energético.

#### Diversidad de Prosumidores
Los datos abarcan dos categorías principales de prosumidores: empresas y particulares. Dentro de estas categorías, existen cuatro tipos de contratos entre los prosumidores y la compañía Eesti Energy, cada uno con condiciones específicas que podrían influir en los patrones de consumo y producción. Esta diversidad en los tipos de contratos y prosumidores enriquece el análisis, permitiendo ajustes y predicciones más precisas según las características contractuales y el tipo de usuario.

## Enriquecimiento de Datos
Para mejorar la capacidad predictiva de mi modelo y capturar la dinámica temporal de los consumos y producciones energéticas, he implementado técnicas avanzadas de enriquecimiento de datos:

### Lagging de Datos (Retraso Temporal)
He incorporado un término de laggeo para las variables de consumo y producción. Este enfoque consiste en crear nuevas variables que representen los valores de días anteriores para cada usuario y cada hora específica. Por ejemplo, para un día n, genero variables adicionales que contienen los datos de consumo y producción de los días n-1, n-2, n-3, y n-4. Esta técnica me permite reconocer patrones y tendencias temporales en el comportamiento energético de los prosumidores, facilitando una predicción más precisa al considerar la influencia de los hábitos y condiciones pasadas.

### Clustering por Condiciones Climáticas
He creado clusters basados en la similitud de las condiciones climáticas que afectan significativamente el consumo y la producción energética. Utilizando técnicas de agrupamiento, seleccioné las variables climáticas más influyentes para definir estos grupos. Posteriormente, agrupé los datos de consumo y producción según estos clusters climáticos. Esto me permite acceder y utilizar los registros de consumo y producción de ocasiones anteriores cuando las condiciones climáticas eran similares, mejorando significativamente la capacidad de predecir cómo variarán el consumo y la producción bajo condiciones climáticas específicas.


## Preprocesamiento
En la etapa de preprocesamiento, he tomado varias decisiones clave para garantizar la precisión y relevancia de los datos utilizados en el modelo. Estas decisiones se centran principalmente en la gestión de los datos meteorológicos y en la definición de las variables objetivo para el consumo y la producción energética.

### Filtrado de Datos Meteorológicos
Dispongo de un dataset que incluye las longitudes y latitudes de diversas estaciones meteorológicas. He realizado un filtrado para eliminar aquellas estaciones que se encuentran fuera de la geografía de Estonia, asegurándome de que los datos climáticos utilizados sean exclusivamente locales. Además, cada estación está asignada a un condado específico. Aunque no conozco la longitud y la latitud exactas de los prosumidores, sí sé en qué condado están ubicados. Por lo tanto, he decidido utilizar como condición climática el valor medio de todas las estaciones meteorológicas dentro del mismo condado. Esto me permite asumir un conjunto uniforme de condiciones climáticas para cada condado, simplificando el modelo al reducir la variabilidad geográfica innecesaria.

### Definición de Variables Objetivo
En cuanto a la producción energética, tengo acceso a la capacidad fotovoltaica instalada de cada prosumidor. Por ello, inicialmente he seleccionado como variable objetivo el "work ratio" de las placas solares, que es el ratio de producción real respecto a la capacidad productiva teórica de cada instalación. Este enfoque me permite evaluar la eficiencia de la producción solar en relación con la capacidad instalada.

Para el consumo, he decidido continuar utilizando los datos en kilovatios-hora (kWh). Esta medida estándar me facilita el análisis y comparación del consumo energético entre diferentes prosumidores y condiciones temporales.

## Análisis Exploratorio de Datos (EDA)
En la fase de Análisis Exploratorio de Datos, he empleado varios métodos para comprender mejor las características y relaciones subyacentes en los datos de producción y consumo energético. Utilicé herramientas gráficas y técnicas estadísticas avanzadas para extraer insights valiosos y dirigir el desarrollo del modelo de predicción.

### Análisis Gráfico
He realizado un análisis gráfico intensivo para observar cómo varían la producción y la variable objetivo a lo largo del tiempo. Esto incluye:

* Variación Diaria: Gráficos que muestran las tendencias de producción y consumo a lo largo de los diferentes días de la semana, identificando patrones recurrentes o anomalías en días específicos.
* Variación Anual: Análisis de cómo cambian la producción y el consumo a lo largo de los días del año, lo cual es crucial para entender el impacto estacional, especialmente relevante en la producción energética solar.
* Variación Horaria: Estudios de cómo fluctúan la producción y el consumo durante las diferentes horas del día, lo que ayuda a identificar los picos de demanda y oferta.
### Análisis de Componentes Principales (PCA)
Para el análisis PCA, utilicé la librería scikit-learn en Python, que facilita la realización de esta técnica estadística. El objetivo era identificar las variables climáticas que tienen mayor impacto en la producción de energía fotovoltaica y en el consumo eléctrico. A través de PCA, pude reducir la dimensionalidad de los conjuntos de datos climáticos, extrayendo las principales componentes que explican la mayor parte de la variabilidad en los datos. Esto no solo simplificó el análisis posterior, sino que también destacó las características climáticas más influyentes que deben ser consideradas en el modelo predictivo.








