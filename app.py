import streamlit as st 
import pandas as pd
import joblib

def predecir():
    data_apredecir = {
    'Pol6TTaCod':[Pol6TTaCod],
    'Capitulo': [Capitulo],
    'VarRC': [VarRC],
    'VarAIR': [VarAIR],
    'modelo': [modelo],
    'diasAseg': [diasAseg],
    'SumaAseg':[SumaAseg],
    'Cobertura':[Cobertura],
    'Bonif':[Bonif],
    'PrimaRC':[PrimaRC],
    'AA':[AA],
    'UNEG':[UNEG]
    }

    # Convertir el diccionario en un DataFrame
    df = pd.DataFrame(data)

    tree_mode = joblib.load('ModeloTarifa.pkl') # Carga del modelo.

    data_apredecir = {
    'Pol6TTaCod':['02_CPLUS'],
    'Capitulo': [1],
    'VarRC': [1],
    'VarAIR': [1],
    'modelo': [2014],
    'diasAseg': [91],
    'SumaAseg':[8000000],
    'Cobertura':['D3%'],
    'Bonif':[0],
    'PrimaRC':[9730.86],
    'AA':[0],
    'UNEG':['IN']
    }
    df_apredecir = pd.DataFrame(data_apredecir)

    # Llama a procedimiento para generar dummies
    d = a_dummies(df_apredecir)

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

    predicciones = tree_mode.predict(X_apredecir)
    # clf_rf.score(X_apredecir, y_train)

    # st.write('La prima Neta Calculada es:', predicciones)



def a_dummies(df_apredecir):
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


#Definir el título
st.title('Mi primer app')

Pol6TTaCod = st.selectbox(
    'Zona de Riesgo',
    ('Zona1', 'Zona2', 'Zona3'))

Capitulo = st.number_input('Capitulo')
VarRC = st.number_input('VarRC')
VarAIR = st.number_input('VarAIR')
modelo = st.number_input('modelo')
diasAseg = st.number_input('diasAseg')
SumaAseg = st.number_input('SumaAseg')
Cobertura = st.text_input('Cobertura')
Bonif = st.number_input('Bonif')
PrimaRC = st.number_input('PrimaRC')
AA = st.number_input('AA')
UNEG = st.text_input('UNEG')

if st.button('Predecir'):
    predecir()