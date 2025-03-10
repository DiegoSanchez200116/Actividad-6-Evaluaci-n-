#Función 1
def cargar_dataset(archivo):
    import pandas as pd # type: ignore
    import os

    # Obtener la extensión del archivo
    extension = os.path.splitext(archivo)[1].lower()
    
    # Cargar el archivo según su extensión
    if extension == '.csv':
        df = pd.read_csv(archivo)
        return(df)
    elif extension == '.xlsx':
        df = pd.read_excel(archivo)
        return(df)
    else:
        raise ValueError(f'Este formato no esta soportado para esta función: {extension}')
    
#Función 2
def sustituir_nulos(df):
    
    import pandas as pd
    #Separo columnas cuantitativas del dataframe
    cuantitativas= df.select_dtypes(include=['float64', 'int64','float','int'])
    #Separo columnas cualitativas del dataframe
    cualitativas = df.select_dtypes(include=['object', 'datetime','category'])
    
    #Sustituimos valores nulos en columnas numéricas
    for i in cuantitativas:
        if i % 2 == 0:
            #Columnas pares
            cuantitativas[i] = cuantitativas[i].fillna(cuantitativas[i].mean())
        else:
            #Columnas impares
            cuantitativas[i] = cuantitativas[i].fillna(99)

    cualitativas = cualitativas.fillna('Este_es_un_valor_nulo')

    # Unimos el dataframe cuantitativo limpio con el dataframe cualitativo
    df = pd.concat([cuantitativas, cualitativas], axis=1)
    return(df)

#Función 3
def cuenta_nulos(df):
    #Valores nulos por columna
    valores_nulos_cols = df.isnull().sum()
    #Valores nulos por dataframe
    valores_nulos_df = df.isnull().sum().sum()
    
    return("Valores nulos por columna", valores_nulos_cols,
            "Valores nulos por dataframe", valores_nulos_df)

#Función 4
def sust_atipicos(df):
    import pandas as pd
    #Separamos las columnas con valores cuantitativos
    cuantitativas = df.select_dtypes(include=['number'])
    cualitativas = df.select_dtypes(include=['object', 'category'])

    #Método aplicando Cuartiles. Encuentro cuartiles 0.25 y 0.75
    y = cuantitativas
    
    percentile25=y.quantile(0.25) #Q1
    percentile75=y.quantile(0.75) #Q3
    iqr=percentile75-percentile25 
    
    Limite_Superior_iqr = percentile75 + 1.5*iqr
    Limite_Inferior_iqr = percentile25 - 1.5*iqr

    df_limpio = cuantitativas[(y<=Limite_Superior_iqr)&(y>=Limite_Inferior_iqr)]

    df_iqr = df_limpio.copy()
    df_iqr = df_iqr.fillna(round(df_limpio.mean(),1))

    df_limpio = pd.concat([cualitativas, df_iqr], axis=1)
    return(df_limpio)
