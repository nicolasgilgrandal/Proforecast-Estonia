import pandas as pd
import numpy as np
import folium
from folium import Map, Circle
import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np
import warnings
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

#-----------------------------------------------------------------------------------------------------------------------------#

"""Función para reconvertir el formato de datetime a dos columnas, una con la fecha, y otra con la hora"""
def separa_hora_fecha(df):
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['hour']=df['datetime'].dt.hour
    df['date']=df['datetime'].dt.date
    df['date']=pd.to_datetime(df['date'])
    df.drop(['datetime'], axis=1, inplace=True)
    return df

#-----------------------------------------------------------------------------------------------------------------------------#

"""Esta función tiene como objetivo asignar cada una de las distintas predicciones climáticas a su cantón 
correspondiente de acuerdo con la latitud y longitud correspondiente"""
def añade_n_canton(clima,ubicacion_n):    
    df_merged=pd.merge(clima, ubicacion_n, on=['longitude', 'latitude'])
    df_merged.drop(['Unnamed: 0'], axis=1, inplace=True)
    return df_merged

#-----------------------------------------------------------------------------------------------------------------------------#

"""Esta función tiene como objetivo la creación de las variables de laggeo seleccionadas. En este caso, se usan 
para la predicción de la producción energética"""
def hacer_shifts_consumo(df, col):
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(by=['prediction_unit_id', 'date', 'hour'], inplace=True)

    # reseteo los índices del dataset en cuestión
    
    df.reset_index(drop=True, inplace=True)
    # aplico shifts de 24, 48, 72 horas y una semana
    df['consumo_shift_1'] = df.groupby(['prediction_unit_id', 'hour'])[col].shift(1)
    df['consumo_shift_2'] = df.groupby(['prediction_unit_id', 'hour'])[col].shift(2)
    df['consumo_shift_3'] = df.groupby(['prediction_unit_id', 'hour'])[col].shift(3)
    df['consumo_shift_7'] = df.groupby(['prediction_unit_id', 'hour'])[col].shift(7)
    df['consumo_shift_clus_1'] = df.groupby(['prediction_unit_id', 'Clusters'])[col].shift(1)
    df['consumo_shift_clus_2'] = df.groupby(['prediction_unit_id', 'Clusters'])[col].shift(2)
    df['consumo_shift_clus_3'] = df.groupby(['prediction_unit_id', 'Clusters'])[col].shift(3)
    df['consumo_shift_clus_4'] = df.groupby(['prediction_unit_id', 'Clusters'])[col].shift(4)
    df=df.dropna()
    return df

#-----------------------------------------------------------------------------------------------------------------------------#

"""Esta función tiene como objetivo la creación de las variables de laggeo seleccionadas. En este caso, se usan 
para la predicción de la producción energética"""
def hacer_shifts_produccion(df, col):
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(by=['prediction_unit_id', 'date', 'hour'], inplace=True)

    # reseteo los índices del dataset en cuestión
    
    df.reset_index(drop=True, inplace=True)
    # aplico shifts de 24, 48, 72 horas y una semana
    df['eficiencia_shift_1'] = df.groupby(['prediction_unit_id', 'hour'])[col].shift(1)
    df['eficiencia_shift_2'] = df.groupby(['prediction_unit_id', 'hour'])[col].shift(2)
    df['eficiencia_shift_3'] = df.groupby(['prediction_unit_id', 'hour'])[col].shift(3)
    df['eficiencia_shift_4'] = df.groupby(['prediction_unit_id', 'hour'])[col].shift(7)
    df['eficiencia_shift_clus_1'] = df.groupby(['prediction_unit_id', 'Clusters'])[col].shift(1)
    df['eficiencia_shift_clus_2'] = df.groupby(['prediction_unit_id', 'Clusters'])[col].shift(2)
    df['eficiencia_shift_clus_3'] = df.groupby(['prediction_unit_id', 'Clusters'])[col].shift(3)
    df['eficiencia_shift_clus_4'] = df.groupby(['prediction_unit_id', 'Clusters'])[col].shift(4)
    df=df.dropna()
    return df

#-----------------------------------------------------------------------------------------------------------------------------#

"""Esta función crea un nuevo dataset donde aparecen las producciones de los distintos usuarios junto con las condiciones
climáticas presentes en ese momento"""
def unir_clima_train(consumo, clima):
    clima_produccion=clima.groupby(['date','hour', 'county']).mean().reset_index()
    df_merged=pd.merge(consumo, clima_produccion, on=['county', 'date', 'hour'])
    return df_merged

#-----------------------------------------------------------------------------------------------------------------------------#

"""Esta función sirve para calcular el work_rate de las instalaciones fotovoltaicas de los distintos usuarios"""
def calcula_eficiencia(df1, df2):
    df_merged=pd.merge(df1, df2, on=['prediction_unit_id', 'data_block_id', 'county', 'is_business', 'product_type'])
    df_merged['date']=df_merged['date_y']
    df_merged.drop(['date_y','date_x'], axis=1,inplace=True)
    df_merged['eficiencia_real']=df_merged['target']/df_merged['installed_capacity']
    df_merged['date'] = pd.to_datetime(df_merged['date'])
    return df_merged

#-----------------------------------------------------------------------------------------------------------------------------#

"""Función para hacer la clusterización de las condiciones climáticas para la producción y añadírselas al dataset"""
def clusterizar_produccion(df_merged, k):
    variables_produccion=df_merged.drop(['eficiencia_real','county','is_business','product_type','target','is_consumption','data_block_id','row_id',
                                     'prediction_unit_id','hour','eic_count','installed_capacity','date']
                                    ,axis=1)
    
    scaler = StandardScaler()
    variables_produccion_scaled = scaler.fit_transform(variables_produccion)

    variables_produccion_scaled = pd.DataFrame(variables_produccion_scaled, columns=variables_produccion.columns)

    kmeans = KMeans(n_clusters=k, random_state=0)
    clusters = kmeans.fit_predict(variables_produccion_scaled)

    variables_produccion_scaled['Cluster'] = clusters
    df_merged['Clusters']=clusters

    

    pca = PCA(n_components=7)  # Reduce a dos dimensiones para la visualización
    principal_components = pca.fit_transform(variables_produccion_scaled.drop('Cluster', axis=1))

    # Crea una visualización de los clusters
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(principal_components[:, 0], principal_components[:, 1], c=variables_produccion_scaled['Cluster'], cmap='viridis', label=variables_produccion_scaled['Cluster'])
    plt.title('Visualización de Clusters K-Means')
    plt.xlabel('Componente Principal 1')
    plt.ylabel('Componente Principal 2')
    plt.colorbar(scatter)
    plt.show()
    return df_merged

#-----------------------------------------------------------------------------------------------------------------------------#

"""Función para hacer la clusterización de las condiciones climáticas para la producción y añadírselas al dataset"""
def clusterizar_consumo(df_merged, k):
    variables_produccion=df_merged.drop(['target','county','is_business','product_type','target','is_consumption','data_block_id','row_id',
                                     'prediction_unit_id','hour','date']
                                    ,axis=1)
    
    scaler = StandardScaler()
    variables_produccion_scaled = scaler.fit_transform(variables_produccion)

    variables_produccion_scaled = pd.DataFrame(variables_produccion_scaled, columns=variables_produccion.columns)

    kmeans = KMeans(n_clusters=k, random_state=0)
    clusters = kmeans.fit_predict(variables_produccion_scaled)

    variables_produccion_scaled['Cluster'] = clusters
    df_merged['Clusters']=clusters

    

    pca = PCA(n_components=7)  # Reduce a dos dimensiones para la visualización
    principal_components = pca.fit_transform(variables_produccion_scaled.drop('Cluster', axis=1))

    # Crea una visualización de los clusters
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(principal_components[:, 0], principal_components[:, 1], c=variables_produccion_scaled['Cluster'], cmap='viridis', label=variables_produccion_scaled['Cluster'])
    plt.title('Visualización de Clusters K-Means')
    plt.xlabel('Componente Principal 1')
    plt.ylabel('Componente Principal 2')
    plt.colorbar(scatter)
    plt.show()
    return df_merged

#-----------------------------------------------------------------------------------------------------------------------------#

def modelo_produccion(df, n_e, m_e, m_s):
    X=df.drop(['target', 'is_consumption', 'data_block_id', 'row_id', 'prediction_unit_id',
          'installed_capacity', 'date', 'eficiencia_real', 'Clusters'], axis=1)
    y=df['eficiencia_real']
    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test, idx_train, idx_test = train_test_split(
        X, y, range(len(y)), test_size=0.2, random_state=42) 

    # Crear y entrenar el modelo
    model = RandomForestRegressor(n_estimators=n_e, max_depth=m_e,min_samples_split=m_s, random_state=42)
    model.fit(X_train, y_train)

    # Predecir el conjunto de prueba
    y_pred = model.predict(X_test)

    # Calcular el error cuadrático medio (MSE) como métrica de evaluación
    mse = mean_squared_error(df['eficiencia_real'].iloc[idx_test], y_pred)
    mae = mean_absolute_error(df['eficiencia_real'].iloc[idx_test], y_pred)

    return mse, mae, idx_train, idx_test, y_pred

#-----------------------------------------------------------------------------------------------------------------------------#

def modelo_consumo(df, n_e, m_e, m_s):
    X=df.drop(['target', 'is_consumption', 'data_block_id', 'row_id', 'prediction_unit_id',
          'date','Clusters'], axis=1)
    y=df['target']
    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test, idx_train, idx_test = train_test_split(
        X, y, range(len(y)), test_size=0.2, random_state=42) 

    # Crear y entrenar el modelo
    model = RandomForestRegressor(n_estimators=n_e, max_depth=m_e,min_samples_split=m_s, random_state=42)
    model.fit(X_train, y_train)

    # Predecir el conjunto de prueba
    y_pred = model.predict(X_test)

    # Calcular el error cuadrático medio (MSE) como métrica de evaluación
    mse = mean_squared_error(df['target'].iloc[idx_test], y_pred)
    mae = mean_absolute_error(df['target'].iloc[idx_test], y_pred)

    return mse, mae, idx_train, idx_test, y_pred




    
    
    
    
    
    
    
    