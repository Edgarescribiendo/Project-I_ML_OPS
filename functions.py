import pandas as pd  

# Cargar los DataFrames desde los archivos parquet
all_data_merge = pd.read_csv("Data/all_data_merge.csv")

# Funcion 1 de desarrollo
def developer(desarrollador):
    if desarrollador not in all_data_merge['developer'].unique():
        return {'error': 'Intente con un desarrollador permitido.'}
    
    # Filtrar el DataFrame para obtener solo las filas donde 'developer' es el desarrollador de entrada
    df_dev = all_data_merge[(all_data_merge['developer'] == desarrollador)].copy()

    # Agrupe por 'release_date', cuente los valores únicos de 'item_id' y cuente la cantidad de valores de 'price' que son 0
    df_dev_group = df_dev.groupby('release_date').agg(
        {'developer': 'count', 'item_id': pd.Series.nunique, 'price': lambda x: (x == 0).sum()}).reset_index()

    # Calcular el porcentaje de contenido gratuito.
    df_dev_group['% contenido free'] = round((df_dev_group['price']/df_dev_group['developer'])*100, 0)

    df_dev_group.rename(columns={'item_id': 'Cantidad de items', 'release_date': 'Año'}, inplace=True)

    # Elimine las columnas 'developer' y 'price'
    df_dev_group.drop('price', axis=1, inplace=True)
    df_dev_group.drop('developer', axis=1, inplace=True)
    
    Final_dicc = {
        "Año": df_dev_group['Año'].to_dict(),
        "Cantidad de items": df_dev_group['Cantidad de items'].tolist(),
        "% contenido free": df_dev_group['% contenido free'].tolist()
    }

    return Final_dicc


def userdata(user_id):

    if user_id not in all_data_merge['user_id'].unique():
        return {'error': 'El usuario mo ha sido identificado.'}
    
    # Filtrar los datos para el usuario especificado
    df_user_data = all_data_merge[all_data_merge['user_id'] == user_id].copy()
    # Calcular la cantidad de dinero gastado por el usuario
    gasto = df_user_data['price'].sum()

    # Calcular el porcentaje de recomendación en base a reviews.recommend
    recomendacion = df_user_data['recommend'].sum()
    porcentaje_recomendacion = recomendacion / len(df_user_data) * 100

    # Calcular la cantidad de items
    cantidad_de_items = df_user_data['item_id'].nunique()

    # Crear un diccionario con los resultados
    resultados = {
        'Cantidad de dinero gastado': gasto,
        'Porcentaje de recomendación': porcentaje_recomendacion,
        'Cantidad de items': cantidad_de_items
    }

    return resultados

def best_developer_year(year: int):
    # Realizar la unión de los DataFrames
    if year not in all_data_merge['year'].unique():
        return {'error': 'El año especificado no existe.'}

    # Filtrar los juegos por año y por recomendación positiva
    df_best_developer_year = all_data_merge[(all_data_merge['year'] == year) & (all_data_merge['recommend'] == True) & (all_data_merge['sentiment_analysis'] == 2)].copy()

    # Contar el número de juegos recomendados por desarrollador y devolver los tres primeros desarrolladores
    top = df_best_developer_year['developer'].value_counts().head(3).index.tolist()

     # Devolver el top 3 de desarrolladores
    return {"Puesto 1" : top[0], "Puesto 2" : top[1], "Puesto 3" : top[2]}
