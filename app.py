import streamlit as st
import plotly.graph_objects as go

st.title("Gráfico Interativo")

col1, col2, col3 = st.columns(3)
with col1:
    st.header("Column 1")
    with st.form("opcao"):
        tipo_opcao = st.radio(
            'Tipo de opção:',
            ['Call', 'Put'],
            captions=['Opção de Compra', 'Opção de Venda']
        )
        operacao = st.radio(
            'Tipo de operação:',
            ['Compra', 'Venda'],
            captions=['Compra de Opção', 'Venda de Opção']
        )
        strike = st.number_input('Strike: ', min_value=0.01, step=0.01)
        premio = st.number_input('Prêmio: ', min_value=0.01, step=0.01)
        submitted = st.form_submit_button("Adicionar")
with col2:
    st.header("Column 2")
    st.write("Content 2")
with col3:
    st.header("Column 3")
    st.write("Content 3")