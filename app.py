import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from model.option import Call, Put
from model.strategy import Strategy


# Init session data
if st.session_state.get('strategy') is None:
    st.session_state.strategy = Strategy()
st.session_state.options = st.session_state.strategy.get_options()

# Main title
st.markdown('<h1 style="text-align: center;">Gráfico de Opções</h1>', unsafe_allow_html=True)

# Build "add option" button's dialog + logic
@st.dialog('Adicionar uma opção')
def add_option():
    name = st.text_input('Identificador: ', value=f'Opção {len(st.session_state.options) + 1}')
    col1, col2 = st.columns(2)
    with col1:
        trade_type = st.radio(
            'Tipo de operação:',
            ['Compra', 'Venda'],
            captions=['Compra de Opção', 'Venda de Opção']
        )
    with col2:
        option_type = st.radio(
            'Tipo de opção:',
            ['Call', 'Put'],
            captions=['Opção de Compra', 'Opção de Venda']
        )
    strike = st.number_input('Strike: ', min_value=0.01, step=0.01)
    premium = st.number_input('Prêmio: ', min_value=0.01, step=0.01)
    quantity = st.number_input('Quantidade: ', min_value=1, step=100, value=100)
    
    col1, col2 = st.columns(2)
    add_button = col1.button('Adicionar', use_container_width=True)
    cancel_button = col2.button('Cancelar', use_container_width=True)
    if add_button:
        option = (
            Call(name, strike, premium, trade_type, quantity) 
            if option_type == 'Call' 
            else Put(name, strike, premium, trade_type, quantity)
        )
        st.session_state.strategy.add_option(option)
        st.session_state.options = st.session_state.strategy.get_options()
        st.rerun()
    if cancel_button:
        st.rerun()

# Build "remove option" button's dialog + logic
@st.dialog('Remover uma opção')
def remove_option():
    options = st.session_state.strategy.get_options()
    if options:
        to_remove = st.radio(
            'Opção a remover:',
            options,
            captions=[option.describe() for option in options]
        )
        st.error(f'A exclusão não poderá ser desfeita.', icon='🚨')
        col1, col2 = st.columns(2)
        confirm = col1.button('Remover', use_container_width=True)
        cancel = col2.button('Cancelar', use_container_width=True)
        if confirm:
            st.session_state.strategy.remove_option(to_remove)
            st.rerun()
        if cancel:
            st.rerun()
    else:
        st.warning(f'Adicione uma opção antes de removê-la.', icon='⚠️')
        close = st.button('Fechar', use_container_width=True)
        if close:
            st.rerun()

# Build "clear" button's dialog + logic
@st.dialog('Confirmação')
def confirm_clear():
    st.error(f'Tem certeza? Todas as opções serão excluídas.', icon='🚨')
    col1, col2 = st.columns(2)
    if col1.button('Confirmar', use_container_width=True):
        st.session_state.strategy.clear_strategy()
        st.session_state.options = st.session_state.strategy.get_options()
        st.rerun()
    if col2.button('Cancelar', use_container_width=True):
        st.rerun()

# Build table view of all options inside the strategy
def view_strategy_table():
    options = st.session_state.options
    if options:
        df = pd.DataFrame(
            [option.get_data() for option in options]
        ).set_index('name')
        # st.data_editor(df, num_rows='dynamic')
        st.dataframe(df, use_container_width=True)
    else:
        st.info(f'Ainda não há opções adicionadas!', icon='💡')

# Build main menu
col1, col2, col3, col4 = st.columns(4)
with col1:
    add_button = st.button('Adicionar Opção', use_container_width=True)
with col2:
    remove_button = st.button('Remover Opção', use_container_width=True)
with col3:
    clear_button = st.button('Limpar Gráfico', use_container_width=True)
with col4:
    view_strategy_table_button = st.toggle('Ver Tabela', value=True, help='Mostra todas as opções adicionadas.') 

if add_button:
    add_option()
if clear_button:
    confirm_clear()
if remove_button:
    remove_option()
if view_strategy_table_button:
    st.subheader('Opções', divider='gray')
    view_strategy_table()

# Build payoff interactive graph
fig = go.Figure()

# Calculate displayed x range based on the min and max strike prices
options = st.session_state.options
min_strike = 0
max_strike = 0
if options:
    min_strike = np.min([option.strike for option in options])
    max_strike = np.max([option.strike for option in options])
    if (max_strike - min_strike) < 1:
        min_strike -= 1
        max_strike += 1
delta = max_strike - min_strike

min_price = np.maximum(min_strike - delta, 0)
max_price = max_strike + delta

# Calculate slider range and default values
min_slider_x_value = 0.0 # Asset price cannot be negative #todo: maybe min_strike / 2 if min_strike > ?? to solve bug when high strike values
max_slider_x_value = (
    max_strike * 2 if max_strike >= 10
    else max_strike + 10
)
selected_slider_x_range = (min_price, max_price)

st.write('')

min_x_selector, max_x_selector = (min_price, max_price)
if options:
    min_x_selector, max_x_selector = st.slider('Intervalo de preço do ativo:', min_slider_x_value, max_slider_x_value, selected_slider_x_range)
else: # disable selector when there are no options on the strategy yet
    st.slider('Intervalo de preço do ativo:', 0.0, 0.0, (0.0, 100.0), disabled=True)

# Add a line on the graph for the resulting payoff
x = np.arange(min_x_selector, max_x_selector, 0.01)
if len(options) > 1:
    y = st.session_state.strategy.calculate_payoff(x).round(2)
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Estratégia'))

# Add a line on the payoff graph for each individual option
i = 1
for option in options:
    y = option.calculate_payoff(x)
    if len(options) > 1:
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=option.name, visible='legendonly'))
    else:
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=option.name)) # is this even necessary??????
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

# Calculate and display metrics
st.subheader('Métricas', divider='gray')
col1, col2, col3, col4 = st.columns(4)
invested_amount = st.session_state.strategy.calculate_invested_amount()
maximum_loss = st.session_state.strategy.calculate_maximum_loss(x)
maximum_profit = st.session_state.strategy.calculate_maximum_profit(x)

col1.metric('Investido (R$)', f'{invested_amount}') #???
if maximum_loss == 0 or invested_amount == 0:
    col2.metric('Perda Máxima (R$)', f'{maximum_loss}')
else:
    col2.metric('Perda Máxima (R$)', f'{maximum_loss}', f'{maximum_loss/abs(invested_amount):.2%}')
if maximum_profit == 0 or invested_amount == 0:
    col3.metric('Ganho Máximo (R$)', f'{maximum_profit}')
else:
    col3.metric('Ganho Máximo (R$)', f'{maximum_profit}', f'{maximum_profit/abs(invested_amount):.2%}')
if maximum_loss != 0:
    max_profit_over_max_loss = abs(maximum_profit)/abs(maximum_loss)
    col4.metric('Ganho/Perda', f'{max_profit_over_max_loss:.1f}x', f'{max_profit_over_max_loss:.2%}')
else:
    col4.metric('Ganho/Perda', '0')
