import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from opcoes.opcao import Call, Put
from opcoes.estrategia import Estrategia


if not st.session_state.get('estrategia'):
    st.session_state.estrategia = Estrategia()
st.session_state.opcoes = st.session_state.estrategia.get_opcoes()

st.markdown('<h1 style="text-align: center;">Gráfico de Opções</h1>', unsafe_allow_html=True)


@st.dialog('Adicionar uma opção')
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
    
    col1, col2 = st.columns(2)
    adicionar = col1.button('Adicionar', use_container_width=True)
    cancelar = col2.button('Cancelar', use_container_width=True)
    if adicionar:
        opcao = (
            Call(nome, strike, premio, operacao, quantidade) 
            if tipo_opcao == 'Call' 
            else Put(nome, strike, premio, operacao, quantidade)
        )
        st.session_state.estrategia.adicionar_opcao(opcao)
        st.session_state.opcoes = st.session_state.estrategia.get_opcoes()
        st.rerun()
    if cancelar:
        st.rerun()
    


@st.dialog('Remover uma opção')
def remover_opcao():
    opcoes = st.session_state.estrategia.get_opcoes()
    if opcoes:
        remover = st.radio(
            'Opção a remover:',
            opcoes,
            captions=[opcao.descrever() for opcao in opcoes]
        )
        st.error(f'A exclusão não poderá ser desfeita.', icon='🚨')
        col1, col2 = st.columns(2)
        confirmar = col1.button('Remover', use_container_width=True)
        cancelar = col2.button('Cancelar', use_container_width=True)
        if confirmar:
            st.session_state.estrategia.remover_opcao(remover)
            st.rerun()
        if cancelar:
            st.rerun()
    else:
        st.warning(f'Adicione uma opção antes de removê-la.', icon='⚠️')
        fechar = st.button('Fechar', use_container_width=True)
        if fechar:
            st.rerun()


@st.dialog('Confirmação')
def confirmar_limpeza():
    st.error(f'Tem certeza? Todas as opções serão excluídas.', icon='🚨')
    col1, col2 = st.columns(2)
    if col1.button('Confirmar', use_container_width=True):
        st.session_state.estrategia.limpar_estrategia()
        st.session_state.opcoes = st.session_state.estrategia.get_opcoes()
        st.rerun()
    if col2.button('Cancelar', use_container_width=True):
        st.rerun()


def ver_estrategia():
    opcoes = st.session_state.opcoes
    if opcoes:
        df = pd.DataFrame(
            [opcao.get_data() for opcao in opcoes]
        ).set_index('nome')
        # st.data_editor(df, num_rows='dynamic')
        st.dataframe(df, use_container_width=True)
    else:
        st.info(f'Ainda não há opções adicionadas!', icon='💡')


col1, col2, col3, col4 = st.columns(4)
with col1:
    adicionar = st.button('Adicionar Opção', use_container_width=True)
with col2:
    remover = st.button('Remover Opção', use_container_width=True)
with col3:
    limpar = st.button('Limpar Gráfico', use_container_width=True)
with col4:
    ver = st.toggle('Ver Tabela', value=True, help='Mostra todas as opções adicionadas.') 

if adicionar:
    adicionar_opcao()
if limpar:
    confirmar_limpeza()
if remover:
    remover_opcao()
if ver:
    st.subheader('Opções', divider='gray')
    ver_estrategia()


fig = go.Figure()

opcoes = st.session_state.opcoes
min_strike = 0
max_strike = 0
if opcoes:
    min_strike = np.min([opcao.strike for opcao in opcoes])
    max_strike = np.max([opcao.strike for opcao in opcoes])
    if (max_strike - min_strike) < 1:
        min_strike -= 1
        max_strike += 1
delta = max_strike - min_strike

menor_preco = np.maximum(min_strike - delta, 0)
maior_preco = max_strike + delta

maior_valor_slider = (
    max_strike * 2 if max_strike >= 10
    else max_strike + 10
)
menor_x, maior_x = (menor_preco, maior_preco)
if opcoes:
    menor_x, maior_x = st.slider('Intervalo de preço do ativo:', 0.0, maior_valor_slider, (menor_preco, maior_preco))
else: # apenas estética
    st.slider('Intervalo de preço do ativo:', 0.0, 0.0, (0.0, 100.0), disabled=True)

x = np.arange(menor_x, maior_x, 0.01)
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

fig.update_yaxes(tickformat='.2f')
fig.update_xaxes(tickformat='.2f')

fig.update_layout(
    title={
        'text': 'Resultado no Vencimento',
        'x': 0.5,
        'xanchor': 'center',
        'font': {
            'size': 18
        }
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


st.subheader('Métricas', divider='gray')
col1, col2, col3, col4 = st.columns(4)
investido = st.session_state.estrategia.calcular_investimento()
perda_maxima = st.session_state.estrategia.calcular_perda_maxima(x)
ganho_maximo = st.session_state.estrategia.calcular_ganho_maximo(x)

col1.metric('Investido (R$)', f'{investido}') #???
if perda_maxima == 0 or investido == 0:
    col2.metric('Perda Máxima (R$)', f'{perda_maxima}')
else:
    col2.metric('Perda Máxima (R$)', f'{perda_maxima}', f'{perda_maxima/abs(investido):.2%}')
if ganho_maximo == 0 or investido == 0:
    col3.metric('Ganho Máximo (R$)', f'{ganho_maximo}')
else:
    col3.metric('Ganho Máximo (R$)', f'{ganho_maximo}', f'{ganho_maximo/abs(investido):.2%}')
if perda_maxima != 0:
    ganho_perda = abs(ganho_maximo)/abs(perda_maxima)
    col4.metric('Ganho/Perda', f'{ganho_perda:.1f}x', f'{ganho_perda:.2%}')
else:
    col4.metric('Ganho/Perda', '0')
