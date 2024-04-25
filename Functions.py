def data_clean (url='Books_df.csv'):
    import pandas as pd
    df = pd.read_csv("Books_df.csv")

    """Sustituimos los espacios por '_', los ':' por nada y el 'no.' por 'num; y colocamos todo en minusculas"""
    df.columns = df.columns.str.replace(" ","_").str.lower().str.replace("no.","num").str.replace(":","")

    """Eliminar las columnas que no necesitamos para el objetivo del proyecto'"""
    df = df.drop(["unnamed_0", 'urls'], axis=1)
    return df

"""Al obtener un dataset en la cual estaba moayoritariamente limpia pasamos al siguiente paso que era crear otra función utilizando API's"""
"""Creamos una función con la que utilizando API buscamos datos para crear diferentes columnas como: autor por API, año de publicación e isbn"""

def read_api(df):
    def buscar_libros(titulo):
        import requests
        base_url = "https://openlibrary.org/search.json"
        params = {'title': titulo}
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            libros = data.get('docs', [])
            resultados = []
            for libro in libros:
                resultados.append({
                'titulo': libro.get('title'),
                'autor': libro.get('author_name', ['Desconocido'])[0],
                'isbn': libro.get('isbn', [None])[0],
                'año_publicacion': libro.get('publish_year', [None])[0]
                })
            
            return resultados
        else:
            return f"Error en la búsqueda: código de estado {response.status_code}"
        
    for i in range (0,len(df)):
        try:
            autor = buscar_libros(df["title"][i])[0]['autor']
            df.loc[i, 'autor_api'] = autor
        
            year_public = buscar_libros(df["title"][i])[0]['año_publicacion']
            df.loc[i, 'year_public'] = year_public

            isbn = buscar_libros(df["title"][i])[0]['isbn']
            df.loc[i, 'isbn'] = isbn
        except:
            None 
    df.csv("df_origin_temp.csv")
    return df

def null_values(df):
    """
    - Al crear las nuevas columnas obtendriamos nuevos valores nulos 
    - Eliminariamos esos nuevos valores nulos 
    - Al hacerlo se nos eliminaria al menos el 80% del dataset principal dejandonos con solo 1234 filas
    """
    df.dropna(subset=["year_public"])
    return df

"""Hacemos el cambio de moneda de rupias a euros"""
def exchange_euro(df):
    from alpha_vantage.foreignexchange import ForeignExchange
    fx = ForeignExchange(key='DCS1WH0CF5CDB755')
    data, _ = fx.get_currency_exchange_rate(from_currency='INR', to_currency='EUR')
    print(data)

    exchange = data['5. Exchange Rate']

    #nueva columna con el precio en euros
    df['price_euro']= (df['price'].str.replace("₹", "").str.replace(",", "").astype(float))*float(exchange)
    return df

