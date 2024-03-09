import streamlit as st
import joblib
import pandas as pd


# Definir la interfaz de la aplicación
def main():
    st.title('Predicción de Prima Neta')

    # Entrada de datos
    st.sidebar.header('Ingrese los datos:')
    #joblib = st.sidebar.text_input('joblib', value=joblib.__version__)
    #sklearn = st.sidebar.text_input('sklearn', value=sklearn.__version__)

    # Cargar datos desde un archivo CSV
    def cargar_datos(nombre_archivo, nombre_hoja):
        datos = pd.read_excel(nombre_archivo, sheet_name=nombre_hoja)
        return datos

    # Nombre del archivo Excel y nombre de la hoja
    nombre_archivo = 'variables.xlsx'

    ltarifas = cargar_datos(nombre_archivo, 'tarifas')
    lUNEG = cargar_datos(nombre_archivo, 'UNEG')
    ldias_aseg = cargar_datos(nombre_archivo, 'Vigencia')
    lCoberturas = cargar_datos(nombre_archivo, 'Coberturas')

    # Mostrar datos en un selectbox
    Pol6TTaCod = st.sidebar.selectbox('Tarifa', ltarifas['Tarifas'], index=None, placeholder="Seleccione una Tarifa")
    capitulo = st.sidebar.number_input('Capitulo', value=1)
    var_rc = st.sidebar.number_input('VarRC', value=1)
    var_air = st.sidebar.number_input('VarAIR', value=1)
    modelo = st.sidebar.number_input('modelo', value=2010)
    dias_aseg = st.sidebar.selectbox('Vigencia', ldias_aseg['Vigencia'], index=None, placeholder="Seleccione una Vigencia")
    suma_aseg = st.sidebar.number_input('SumaAseg', value=6259000)
    Cobertura = st.sidebar.selectbox('Cobertura', lCoberturas['Coberturas'], index=None, placeholder="Seleccione una Cobertura")
    bonif = st.sidebar.number_input('Bonif', value=0.0)
    aa = st.sidebar.number_input('AA', value=0)
    PrimaRC = st.sidebar.number_input('PrimaRC', value=10814.18)
    UNEG = st.sidebar.selectbox('Unidad de Negocios', lUNEG['UNEG'], index=None, placeholder="Seleccione una Unidad de Negocios")

    # Botón para predecir
    if st.sidebar.button('Predecir Prima Neta'):
        data_apredecir = {
            'Pol6TTaCod':[Pol6TTaCod],
            'Capitulo': [capitulo],
            'VarRC': [var_rc],
            'VarAIR': [var_air],
            'modelo': [modelo],
            'diasAseg': [dias_aseg],
            'SumaAseg': [suma_aseg],
            'Cobertura': [Cobertura],
            'Bonif': [bonif],
            'PrimaRC': [PrimaRC],
            'AA': [aa],
            'UNEG': [UNEG]
        }
        
        # Cargar el modelo
        # modelo = load('ModeloTarifa.pkl')

        data = {
            'Capitulo': [],
            'VarRC': [],
            'VarAIR': [],
            'modelo': [],
            'diasAseg': [],
            'SumaAseg': [],
            'Bonif': [],
            'AA': [],
            'PrimaRC': [],
            'COB_A': [],
            'COB_A2': [],
            'COB_B': [],
            'COB_B1': [],
            'COB_B3': [],
            'COB_C': [],
            'COB_C1': [],
            'COB_C1+': [],
            'COB_C2': [],
            'COB_C3': [],
            'COB_D1%': [],
            'COB_D2': [],
            'COB_D2%': [],
            'COB_D2I': [],
            'COB_D3': [],
            'COB_D3%': [],
            'COB_D32': [],
            'COB_D36': [],
            'COB_D3I': [],
            'COB_D4%': [],
            'COB_D4I': [],
            'COB_D5%': [],
            'COB_D54': [],
            'COB_D6': [],
            'COB_D6%': [],
            'TAR_01': [],
            'TAR_01_21': [],
            'TAR_01_CPLUS': [],
            'TAR_02': [],
            'TAR_02_21': [],
            'TAR_02_CPLUS': [],
            'TAR_02_FOODT': [],
            'TAR_03': [],
            'TAR_03_21': [],
            'TAR_03_CPLUS': [],
            'TAR_04': [],
            'TAR_04_21': [],
            'TAR_04_CPLUS': [],
            'TAR_05': [],
            'TAR_05_21': [],
            'TAR_05_CPLUS': [],
            'TAR_06': [],
            'TAR_06_21': [],
            'TAR_06_CPLUS': [],
            'TAR_07': [],
            'TAR_07_21': [],
            'TAR_07_CPLUS': [],
            'TAR_08': [],
            'TAR_08_21': [],
            'TAR_08_CPLUS': [],
            'TAR_09': [],
            'TAR_09_21': [],
            'TAR_09_CPLUS': [],
            'TAR_13': [],
            'TAR_13_21': [],
            'TAR_13_CPLUS': [],
            'TAR_15': [],
            'TAR_15_21': [],
            'TAR_15_CPLUS': [],
            'TAR_16_CPLUS': [],
            'TAR_18': [],
            'TAR_18_21': [],
            'TAR_19': [],
            'TAR_19_CPLUS': [],
            'TAR_23': [],
            'TAR_23_21': [],
            'TAR_23_CPLUS': [],
            'UNEG_BA': [],
            'UNEG_IN': [],
            'UNEG_CB': []
        }

        # Convertir el diccionario en un DataFrame
        df = pd.DataFrame(data)

        model = joblib.load('RF_ModeloTarifa.pkl')

        df_apredecir = pd.DataFrame(data_apredecir)

        # Dummies para coberturas
        dummy_columns = {
            'Cobertura': {
                'prefix': 'COB',
                'sep': ';'
            }
        }

        for column_name, dummy_data in dummy_columns.items():
            dummies = df_apredecir[column_name].str.get_dummies(sep=dummy_data['sep'])

            dummies.columns = map(lambda col: f'{dummy_data["prefix"]}_{col}', dummies.columns)

            df_apredecir = pd.concat([df_apredecir, dummies], axis=1)

        df_apredecir = df_apredecir.drop(columns=dummy_columns.keys())

        # Dummies para Tarifa
        dummy_columns = {
            'Pol6TTaCod': {
                'prefix': 'TAR',
                'sep': ';'
            }
        }

        for column_name, dummy_data in dummy_columns.items():
            dummies = df_apredecir[column_name].str.get_dummies(sep=dummy_data['sep'])

            dummies.columns = map(lambda col: f'{dummy_data["prefix"]}_{col}', dummies.columns)

            df_apredecir = pd.concat([df_apredecir, dummies], axis=1)

        df_apredecir = df_apredecir.drop(columns=dummy_columns.keys())

        # Dummies para UNEG
        dummy_columns = {
            'UNEG': {
                'prefix': 'UNEG',
                'sep': ';'
            }
        }

        for column_name, dummy_data in dummy_columns.items():
            dummies = df_apredecir[column_name].str.get_dummies(sep=dummy_data['sep'])

            dummies.columns = map(lambda col: f'{dummy_data["prefix"]}_{col}', dummies.columns)

            df_apredecir = pd.concat([df_apredecir, dummies], axis=1)

        df_apredecir = df_apredecir.drop(columns=dummy_columns.keys())

        # Crear un DataFrame vacío con la misma estructura que A ----------------------------------------------------
        df_final = pd.DataFrame(columns=df.columns)

        C = df_final.copy()

        columnas_comunes = set(df_final.columns) & set(df_apredecir.columns)
        C[list(columnas_comunes)] = df_apredecir[list(columnas_comunes)]

        # Rellenar los valores faltantes en C con ceros
        columnas_faltantes = set(df_final.columns) - set(df_apredecir.columns)
        for columna in columnas_faltantes:
            C[columna] = 0

        # Suponiendo que df_apredecir es tu nuevo conjunto de datos con las mismas características que los datos de entrenamiento
        # y que deseas predecir la variable 'PrimaNeta'
        X_apredecir = C[['Capitulo',	'VarRC',	'VarAIR',	'modelo',	'diasAseg',	'SumaAseg',	'Bonif',	'AA',	'PrimaRC',	'COB_A',	'COB_A2',	'COB_B',	'COB_B1',	'COB_B3',	'COB_C',	'COB_C1',	'COB_C1+',	'COB_C2',	'COB_C3',	'COB_D1%',	'COB_D2',	'COB_D2%',	'COB_D2I',	'COB_D3',	'COB_D3%',	'COB_D32',	'COB_D36',	'COB_D3I',	'COB_D4%',	'COB_D4I',	'COB_D5%',	'COB_D54',	'COB_D6',	'COB_D6%',	'TAR_01',	'TAR_01_21',	'TAR_01_CPLUS',	'TAR_02',	'TAR_02_21',	'TAR_02_CPLUS',	'TAR_02_FOODT',	'TAR_03',	'TAR_03_21',	'TAR_03_CPLUS',	'TAR_04',	'TAR_04_21',	'TAR_04_CPLUS',	'TAR_05',	'TAR_05_21',	'TAR_05_CPLUS',	'TAR_06',	'TAR_06_21',	'TAR_06_CPLUS',	'TAR_07',	'TAR_07_21',	'TAR_07_CPLUS',	'TAR_08',	'TAR_08_21',	'TAR_08_CPLUS',	'TAR_09',	'TAR_09_21',	'TAR_09_CPLUS',	'TAR_13',	'TAR_13_21',	'TAR_13_CPLUS',	'TAR_15',	'TAR_15_21',	'TAR_15_CPLUS',	'TAR_16_CPLUS',	'TAR_18',	'TAR_18_21',	'TAR_19',	'TAR_19_CPLUS',	'TAR_23',	'TAR_23_21',	'TAR_23_CPLUS', 'UNEG_BA', 'UNEG_IN', 'UNEG_CB']]

        predicciones = model.predict(X_apredecir)
        
        st.info(f'La PrimaNeta calculada es de: $ {round(predicciones[0], 2)}')

if __name__ == '__main__':
    main()