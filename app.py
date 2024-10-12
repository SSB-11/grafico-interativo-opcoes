import numpy as np
import streamlit as st
import plotly.graph_objects as go

from opcoes.opcao import Call, Put
from opcoes.estrategia import Estrategia


if not st.session_state.get('estrategia'):
    st.session_state.estrategia = Estrategia()


@st.dialog("Adicione uma opção")
def adicionar_opcao():
    col1, col2 = st.columns(2)
    with col1:
        tipo_opcao = st.radio(
            'Tipo de opção:',
            ['Call', 'Put'],
            captions=['Opção de Compra', 'Opção de Venda']
        )
    with col2:
        operacao = st.radio(
            'Tipo de operação:',
            ['Compra', 'Venda'],
            captions=['Compra de Opção', 'Venda de Opção']
        )
    strike = st.number_input('Strike: ', min_value=0.01, step=0.01)
    premio = st.number_input('Prêmio: ', min_value=0.01, step=0.01)
    quantidade = st.number_input('Quantidade: ', min_value=1, step=100, value=100)
    submitted = st.button("Adicionar")
    if submitted:
        opcao = (
            Call(strike, premio, operacao, quantidade) 
            if tipo_opcao == 'Call' 
            else Put(strike, premio, operacao, quantidade)
        )
        st.session_state.estrategia.adicionar_opcao(opcao)
        st.rerun()

column1, column2, column3 = st.columns([1, 2, 1])
with column1:
    adicionar = st.button("Adicionar Opção")
    limpar = st.button("Limpar Gráfico")
    if adicionar:
        adicionar_opcao()
    if limpar:
        st.session_state.estrategia.limpar_estrategia()

fig = go.Figure()
i = 1
for opcao in st.session_state.estrategia.get_opcoes():
    x = np.arange(opcao.strike - 2, 14, 0.01)
    y = opcao.calcular_payoff(x)
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=f'Opcão {i}'))
    i += 1

fig.update_yaxes(tickformat=".2f")
fig.update_xaxes(tickformat=".2f")

fig.update_layout(
    title={
        'text': 'Resultado no Vencimento',
        'x': 0.5,
        'xanchor': 'center'
    },
    xaxis_title='Preço do Ativo (R$)',
    yaxis_title='Lucro/Prejuízo (R$)',
    width=800,
    height=600,
    template='plotly_dark'
)

with column2:
    # st.title("Gráfico Interativo")
    st.markdown("<h1 style='text-align: center;'>Gráfico Interativo</h1>", unsafe_allow_html=True)
    st.plotly_chart(fig)
