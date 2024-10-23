import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from opcoes.opcao import Call, Put
from opcoes.estrategia import Estrategia


if not st.session_state.get('estrategia'):
    st.session_state.estrategia = Estrategia()

st.session_state.opcoes = st.session_state.estrategia.get_opcoes()
st.markdown("<h1 style='text-align: center;'>Gráfico Interativo</h1>", unsafe_allow_html=True)

@st.dialog("Adicionar uma opção")
def adicionar_opcao():
    nome = st.text_input('Identificador: ', value=f'Opção {len(st.session_state.opcoes) + 1}')
    col1, col2 = st.columns(2)
    with col1:
        operacao = st.radio(
            'Tipo de operação:',
            ['Compra', 'Venda'],
            captions=['Compra de Opção', 'Venda de Opção']
        )
    with col2:
        tipo_opcao = st.radio(
            'Tipo de opção:',
            ['Call', 'Put'],
            captions=['Opção de Compra', 'Opção de Venda']
        )
    strike = st.number_input('Strike: ', min_value=0.01, step=0.01)
    premio = st.number_input('Prêmio: ', min_value=0.01, step=0.01)
    quantidade = st.number_input('Quantidade: ', min_value=1, step=100, value=100)
    submitted = st.button("Adicionar")
    if submitted:
        opcao = (
            Call(nome, strike, premio, operacao, quantidade) 
            if tipo_opcao == 'Call' 
            else Put(nome, strike, premio, operacao, quantidade)
        )
        st.session_state.estrategia.adicionar_opcao(opcao)
        st.session_state.opcoes = st.session_state.estrategia.get_opcoes()
        st.rerun()


@st.dialog("Remover uma opção")
def remover_opcao():
    opcoes = st.session_state.estrategia.get_opcoes()
    if opcoes:
        st.warning(f'A exclusão não poderá ser desfeita.', icon='⚠️')
    remover = st.radio(
        'Opção a remover:',
        opcoes
    )
    submitted = st.button("Remover")
    if submitted:
        st.session_state.estrategia.remover_opcao(remover)
        st.rerun()


# @st.dialog("Sua estratégia:")
def ver_estrategia():
    if not st.session_state.get('view_strategy'):
        st.session_state.view_strategy = True
        opcoes = st.session_state.opcoes
        if opcoes:
            df = pd.DataFrame(
                [opcao.get_data() for opcao in opcoes]
            ).set_index('nome')
            # st.data_editor(df, num_rows='dynamic')
            st.table(df)
        else:
            st.write('Ainda não há opções em sua estratégia!')
    else:
        st.session_state.view_strategy = False
        st.write(st.session_state.view_strategy)
        st.rerun()


col1, col2, col3, col4 = st.columns(4)
with col1:
        ver = st.button('Ver Estratégia') 
with col2:
    adicionar = st.button('Adicionar Opção')
with col3:
    remover = st.button('Remover Opção')
with col4:
    limpar = st.button('Limpar Gráfico')

if adicionar:
    adicionar_opcao()
if ver:
    ver_estrategia()
if limpar:
    st.session_state.estrategia.limpar_estrategia()
    st.session_state.opcoes = st.session_state.estrategia.get_opcoes()
if remover:
    remover_opcao()


fig = go.Figure()

opcoes = st.session_state.opcoes
min_strike = 0
max_strike = 0
if opcoes:
    min_strike = np.min([opcao.strike for opcao in opcoes])
    max_strike = np.max([opcao.strike for opcao in opcoes])
    if (min_strike - max_strike) < 1:
        min_strike -= 1
        max_strike += 1
delta = max_strike - min_strike

x = np.arange(min_strike - delta, max_strike + delta, 0.01)
if len(opcoes) > 1:
    y = st.session_state.estrategia.calcular_payoff(x).round(2)
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Estratégia'))

i = 1
for opcao in opcoes:
    y = opcao.calcular_payoff(x)
    if len(opcoes) > 1:
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=opcao.nome, visible='legendonly'))
    else:
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=opcao.nome)) # is this even necessary??????
    i += 1

fig.update_yaxes(tickformat=".2f")
fig.update_xaxes(tickformat=".2f")

fig.update_layout(
    title={
        'text': 'Resultado no Vencimento',
        'x': 0.5,
        'xanchor': 'center'
    },
    # xaxis={
    #     'range': [min_strike - delta, max_strike + delta]
    # },
    xaxis_title='Preço do Ativo (R$)',
    yaxis_title='Lucro/Prejuízo (R$)',
    width=800,
    height=600,
    template='plotly_dark'
)

st.plotly_chart(fig)

col1, col2, col3 = st.columns(3)
col1.metric("Custo", st.session_state.estrategia.calcular_custo())
col2.metric("Perda Máxima", st.session_state.estrategia.calcular_perda_maxima())