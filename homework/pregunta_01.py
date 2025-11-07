"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"
    """
    import pandas as pd
    import os

    def cargar_datos(ruta: str) -> pd.DataFrame:
        return pd.read_csv(ruta, sep=';', index_col=0)

    def normalizar_sexo(df: pd.DataFrame) -> pd.DataFrame:
        df['sexo'] = df['sexo'].astype('category').str.lower()
        return df

    def limpiar_fecha(df: pd.DataFrame) -> pd.DataFrame:
        df['fecha_de_beneficio'] = pd.to_datetime(
            df['fecha_de_beneficio'], format="%d/%m/%Y", errors="coerce"
        ).combine_first(
            pd.to_datetime(df['fecha_de_beneficio'], format="%Y/%m/%d", errors="coerce")
        )
        return df

    def limpiar_monto(df: pd.DataFrame) -> pd.DataFrame:
        df['monto_del_credito'] = (
            df['monto_del_credito']
            .str.strip()
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.replace(".00", "", regex=False)
            .astype(int)
        )
        return df

    def normalizar_columnas(df: pd.DataFrame, columnas_strip: list, columnas_no_strip: list) -> pd.DataFrame:
        for col in columnas_no_strip:
            if col in df.columns:
                df[col] = (
                    df[col]
                    .str.lower()
                    .str.replace("_", " ", regex=False)
                    .str.replace("-", " ", regex=False)
                )
        for col in columnas_strip:
            if col in df.columns:
                df[col] = (
                    df[col]
                    .str.lower()
                    .str.replace("_", " ", regex=False)
                    .str.replace("-", " ", regex=False)
                    .str.strip()
                )
        return df

    def eliminar_datos_invalidos(df: pd.DataFrame) -> pd.DataFrame:
        df = df.drop_duplicates()
        df = df.dropna()
        return df

    def exportar(df: pd.DataFrame, ruta: str):
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        df.to_csv(ruta, sep=';', index=True)


    def solucion():
        df = cargar_datos('files/input/solicitudes_de_credito.csv')
        df = normalizar_sexo(df)
        df = limpiar_fecha(df)
        df = limpiar_monto(df)

        columnas_no_strip = ['barrio']
        columnas_strip = ['idea_negocio', 'línea_credito', 'tipo_de_emprendimiento']
        df = normalizar_columnas(df, columnas_strip, columnas_no_strip)

        df = eliminar_datos_invalidos(df)
        exportar(df, 'files/output/solicitudes_de_credito.csv')

    solucion()


