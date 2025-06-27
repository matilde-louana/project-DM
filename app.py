# Importar bibliotecas
import streamlit as st
import pandas as pd
import joblib


st.header("Previsão de Reclamação de Seguro Automóvel")
st.subheader("Classificação com modelo treinado")

age_dict = {'16-25': 0, '26-39': 1, '40-64': 2, '65+': 3}
exp_dict = {'0-9y': 0, '10-19y': 1, '20-29y': 2, '30y+': 3}
edu_dict = {'none': 0, 'high school': 1, 'university': 2}
inc_dict = {'poverty': 0, 'working class': 1, 'middle class': 2, 'upper class': 3}
year_dict = {'before 2015': 0, 'after 2015': 1}

age = st.selectbox("Idade", list(age_dict.keys()))
driving_exp = st.selectbox("Experiência de condução", list(exp_dict.keys()))
education = st.selectbox("Educação", list(edu_dict.keys()))
income = st.selectbox("Rendimento", list(inc_dict.keys()))
vehicle_year = st.selectbox("Ano do veículo", list(year_dict.keys()))

gender = st.selectbox("Género", ['Feminino', 'Masculino'])
vehicle_type = st.selectbox("Tipo de veículo", ['Sedan', 'Desportivo'])

credit_score = st.number_input("Credit Score", min_value=0.0)
vehicle_ownership = st.selectbox("É proprietário do veículo?", ['Não', 'Sim'])
married = st.selectbox("É casado(a)?", ['Não', 'Sim'])
children = st.selectbox("Tem filhos?", ['Não', 'Sim'])

annual_mileage = st.number_input("Quilometragem anual", min_value=0.0)
speeding_violations = st.number_input("Nº infrações de velocidade", min_value=0)
duis = st.number_input("Nº de DUIs", min_value=0)
past_accidents = st.number_input("Nº de acidentes anteriores", min_value=0)

age = age_dict[age]
driving_exp = exp_dict[driving_exp]
education = edu_dict[education]
income = inc_dict[income]
vehicle_year = year_dict[vehicle_year]

gender_male = 1 if gender == 'Masculino' else 0
vehicle_type_sportscar = 1 if vehicle_type == 'Desportivo' else 0
vehicle_ownership = 1 if vehicle_ownership == 'Sim' else 0
married = 1 if married == 'Sim' else 0
children = 1 if children == 'Sim' else 0

if st.button("Prever Reclamação"):

    modelo = joblib.load("modelo_final.pkl")

    df = pd.DataFrame([[
        age, driving_exp, education, income, vehicle_year,
        gender_male, vehicle_type_sportscar,
        credit_score, vehicle_ownership, married, children,
        annual_mileage, speeding_violations, duis, past_accidents
    ]], columns=[
        'AGE', 'DRIVING_EXPERIENCE', 'EDUCATION', 'INCOME', 'VEHICLE_YEAR',
        'GENDER_male', 'VEHICLE_TYPE_sports car',
        'CREDIT_SCORE', 'VEHICLE_OWNERSHIP', 'MARRIED', 'CHILDREN',
        'ANNUAL_MILEAGE', 'SPEEDING_VIOLATIONS', 'DUIS', 'PAST_ACCIDENTS'
    ])

    st.dataframe(df)

    prediction = modelo.predict(df)[0]

    st.subheader("Resultado da Previsão:")
    if prediction == 1:
        st.error("O cliente  irá apresentar uma reclamação.")
    else:
        st.success("O cliente **não** irá apresentar reclamação.")
