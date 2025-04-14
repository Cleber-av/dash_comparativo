
import pandas as pd
import plotly.express as px
import streamlit as st

# Carregar os dados
df = pd.read_excel("Comparativo_Tipo_Final.xlsx")

# Conversão da coluna de data (ajuste conforme nome da coluna)
df['DATA'] = pd.to_datetime(df['DATA'])

# Sidebar com filtros
st.sidebar.title("Filtros")

tipos = df['TIPO FINAL'].unique()
tipo_escolhido = st.sidebar.selectbox("Selecione o Tipo Final", tipos)
data_range = st.sidebar.date_input("Selecione o Período", [df['DATA'].min(), df['DATA'].max()])

# Filtrar os dados com base nas escolhas
filtro = (df['TIPO FINAL'] == tipo_escolhido) & (df['DATA'] >= pd.to_datetime(data_range[0])) & (df['DATA'] <= pd.to_datetime(data_range[1]))
df_filtrado = df[filtro]

# Período do ano anterior para comparação
ano_atual = data_range[0].year
ano_anterior = ano_atual - 1
data_inicio_ano_ant = data_range[0].replace(year=ano_anterior)
data_fim_ano_ant = data_range[1].replace(year=ano_anterior)

filtro_ano_ant = (df['TIPO FINAL'] == tipo_escolhido) & (df['DATA'] >= data_inicio_ano_ant) & (df['DATA'] <= data_fim_ano_ant)
df_ano_ant = df[filtro_ano_ant]

# Total de ocorrências
total_atual = df_filtrado.shape[0]
total_anterior = df_ano_ant.shape[0]
variacao = ((total_atual - total_anterior) / total_anterior * 100) if total_anterior > 0 else 0

# Layout
st.title("Dashboard Interativo - Tipo Final")
st.metric("Total Atual", total_atual)
st.metric("Total Ano Anterior", total_anterior)
st.metric("Variação (%)", f"{variacao:.2f}%")

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
