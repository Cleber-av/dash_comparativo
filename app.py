import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime

# Carregar os dados
df = pd.read_excel("Comparativo_Tipo_Final.xlsx")

# Conversão da coluna de data
df['DATA'] = pd.to_datetime(df['DATA'])

# Sidebar com filtros
st.sidebar.title("Filtros")

tipos = df['TIPO FINAL'].unique()
tipo_escolhido = st.sidebar.selectbox("Selecione o Tipo de Ocorrência", tipos)
data_range = st.sidebar.date_input("Selecione o Período", df['DATA'].min(['DATA'].dt.year == 2025), df['DATA'].max(['DATA'].dt.year == 2025))


# Garantir que o período sempre tenha dois valores
if len(data_range) != 2:
    st.error("Por favor, selecione um intervalo de datas válido.")
    st.stop()
    
# Filtrar os dados com base nas escolhas
data_inicio = pd.to_datetime(data_range[0])
data_fim = pd.to_datetime(data_range[1])

filtro = (
    (df['TIPO FINAL'] == tipo_escolhido) &
    (df['DATA'] >= data_inicio) &
    (df['DATA'] <= data_fim)
)
df_filtrado = df[filtro]

# Período do ano anterior para comparação
ano_anterior = data_inicio.year - 1
delta = data_fim - data_inicio

data_inicio_ano_ant = data_inicio.replace(year=ano_anterior)
data_fim_ano_ant = data_inicio_ano_ant + delta

filtro_ano_ant = (
    (df['TIPO FINAL'] == tipo_escolhido) &
    (df['DATA'] >= data_inicio_ano_ant) &
    (df['DATA'] <= data_fim_ano_ant)
)
df_ano_ant = df[filtro_ano_ant]

# Total de ocorrências
df_2025 = df[(df['DATA'].dt.year == 2025)]
total_2025 = df_2025[df_2025['TIPO FINAL'] == tipo_escolhido].shape[0]
filtrado_2025 = df_filtrado.shape[0]
total_atual = df_filtrado.shape[0]
total_anterior = df_ano_ant.shape[0]
variacao = ((filtrado_2025 - total_anterior) / total_anterior * 100) if total_anterior > 0 else 0

# Total por tipo final apenas para ano 2024
df_2024 = df[(df['DATA'].dt.year == 2024)]
total_2024 = df_2024[df_2024['TIPO FINAL'] == tipo_escolhido].shape[0]

# Layout
st.title("Dashboard Interativo - Ocorrências GCM")
st.metric("Total do Período Selecionado", filtrado_2025)
st.metric("Total Ano Anterior mesmo período", total_anterior)
st.metric("Variação (%)", f"{variacao:.2f}%")

st.subheader("Total de Ocorrências do Ano")
st.metric("Total 2025", total_2025)
st.metric("Total 2024", total_2024)


# Gráfico de linha comparativo
comparativo_df = pd.concat([
    df_filtrado.assign(Período='Atual'),
    df_ano_ant.assign(Período='Ano Anterior')
])

fig = px.histogram(
    comparativo_df,
    x='DATA',
    color='Período',
    barmode='group',
    title=f"Comparativo Temporal para {tipo_escolhido}"
)

st.plotly_chart(fig)

# Tabela com dados filtrados
st.dataframe(df_filtrado.sort_values(by='DATA', ascending=False))
