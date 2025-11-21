import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from model.option import Call, Put
from model.strategy import Strategy
from utils.i18n import I18N


# Init session data
if st.session_state.get('strategy') is None:
    st.session_state.strategy = Strategy()
st.session_state.options = st.session_state.strategy.get_options()

# Init translator
i18n = I18N('pt') # for now, assume selected language is portuguese

# Main title
st.markdown(f'<h1 style="text-align: center;">{i18n.t("app.title")}</h1>', unsafe_allow_html=True)

# Build "add option" button's dialog + logic
@st.dialog(i18n.t('dialog.add.title'))
def add_option():
    name = st.text_input(f'{i18n.t("dialog.add.input.text.id.label")}: ', value=f'{i18n.t("dialog.add.input.text.id.placeholder")} {len(st.session_state.options) + 1}')
    col1, col2 = st.columns(2)
    with col1:
        trade_type = st.radio(
            i18n.t('dialog.add.input.radio.tradeType.label') + ':',
            [i18n.t('dialog.add.input.radio.tradeType.buy.value'), i18n.t('dialog.add.input.radio.tradeType.sell.value')],
            captions=[i18n.t('dialog.add.input.radio.tradeType.buy.caption'), i18n.t('dialog.add.input.radio.tradeType.sell.caption')]
        )
    with col2:
        option_type = st.radio(
            i18n.t('dialog.add.input.radio.optionType.label') + ':',
            [i18n.t('dialog.add.input.radio.optionType.call.value'), i18n.t('dialog.add.input.radio.optionType.put.value')],
            captions=[i18n.t('dialog.add.input.radio.optionType.call.caption'), i18n.t('dialog.add.input.radio.optionType.put.caption')]
        )
    strike = st.number_input(i18n.t('dialog.add.input.number.strike.label') + ': ', min_value=0.01, step=0.01)
    premium = st.number_input(i18n.t('dialog.add.input.number.premium.label') + ': ', min_value=0.01, step=0.01)
    quantity = st.number_input(i18n.t('dialog.add.input.number.quantity.label') + ': ', min_value=1, step=100, value=100)
    
    col1, col2 = st.columns(2)
    add_button = col1.button(i18n.t('btn.add'), use_container_width=True)
    cancel_button = col2.button(i18n.t('btn.cancel'), use_container_width=True)
    if add_button:
        option = (
            Call(name, strike, premium, trade_type, quantity) 
            if option_type == i18n.t('dialog.add.input.radio.optionType.call.value')
            else Put(name, strike, premium, trade_type, quantity)
        )
        st.session_state.strategy.add_option(option)
        st.session_state.options = st.session_state.strategy.get_options()
        st.rerun()
    if cancel_button:
        st.rerun()

# Build "remove option" button's dialog + logic
@st.dialog(i18n.t('dialog.delete.title'))
def remove_option():
    options = st.session_state.strategy.get_options()
    if options:
        to_remove = st.radio(
            i18n.t('dialog.delete.input.radio.label') + ':',
            options,
            captions=[option.describe() for option in options]
        )
        st.error(i18n.t('warning.dialog.delete.irreversible'), icon='🚨')
        col1, col2 = st.columns(2)
        remove = col1.button(i18n.t('btn.delete'), use_container_width=True)
        cancel = col2.button(i18n.t('btn.cancel'), use_container_width=True)
        if remove:
            st.session_state.strategy.remove_option(to_remove)
            st.rerun()
        if cancel:
            st.rerun()
    else:
        st.warning(i18n.t('warning.dialog.delete.noOptionsYet'), icon='⚠️')
        close = st.button(i18n.t('btn.close'), use_container_width=True)
        if close:
            st.rerun()

# Build "clear" button's dialog + logic
@st.dialog(i18n.t('dialog.clear.title'))
def confirm_clear():
    st.error(i18n.t('warning.dialog.delete.confirmation'), icon='🚨')
    col1, col2 = st.columns(2)
    if col1.button(i18n.t('btn.confirm'), use_container_width=True):
        st.session_state.strategy.clear_strategy()
        st.session_state.options = st.session_state.strategy.get_options()
        st.rerun()
    if col2.button(i18n.t('btn.cancel'), use_container_width=True):
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
        st.info(i18n.t('table.toggle.warning.noOptionsYet'), icon='💡')

# Build main menu
col1, col2, col3, col4 = st.columns(4)
with col1:
    add_button = st.button(i18n.t('dialog.add.title'), use_container_width=True)
with col2:
    remove_button = st.button(i18n.t('dialog.delete.title'), use_container_width=True)
with col3:
    clear_button = st.button(i18n.t('btn.clear'), use_container_width=True)
with col4:
    view_strategy_table_button = st.toggle(i18n.t('table.toggle.title'), value=True, help=i18n.t('table.toggle.hint')) 

if add_button:
    add_option()
if clear_button:
    confirm_clear()
if remove_button:
    remove_option()
if view_strategy_table_button:
    st.subheader(i18n.t('table.title'), divider='gray')
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
    min_x_selector, max_x_selector = st.slider(i18n.t('slider.input.label') + ':', min_slider_x_value, max_slider_x_value, selected_slider_x_range)
else: # disable selector when there are no options on the strategy yet
    st.slider(i18n.t('slider.input.label') + ':', 0.0, 0.0, (0.0, 100.0), disabled=True)

# Add a line on the graph for the resulting payoff
x = np.arange(min_x_selector, max_x_selector, 0.01)
if len(options) > 1:
    y = st.session_state.strategy.calculate_payoff(x).round(2)
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=i18n.t('graph.line.strategy')))

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
        'text': i18n.t('graph.title'),
        'x': 0.5,
        'xanchor': 'center',
        'font': {
            'size': 18
        }
    },
    # xaxis={
    #     'range': [min_strike - delta, max_strike + delta]
    # },
    xaxis_title=i18n.t('graph.xaxis.title'),
    yaxis_title=i18n.t('graph.yaxis.title'),
    width=800,
    height=600,
    template='plotly_dark'
)

st.plotly_chart(fig)

# Calculate and display metrics
st.subheader(i18n.t('metrics.title'), divider='gray')
col1, col2, col3, col4 = st.columns(4)
invested_amount = st.session_state.strategy.calculate_invested_amount()
maximum_loss = st.session_state.strategy.calculate_maximum_loss(x)
maximum_profit = st.session_state.strategy.calculate_maximum_profit(x)

col1.metric(i18n.t('metrics.label.invested'), f'{invested_amount}') #???
if maximum_loss == 0 or invested_amount == 0:
    col2.metric(i18n.t('metrics.label.maxLoss'), f'{maximum_loss}')
else:
    col2.metric(i18n.t('metrics.label.maxLoss'), f'{maximum_loss}', f'{maximum_loss/abs(invested_amount):.2%}')
if maximum_profit == 0 or invested_amount == 0:
    col3.metric(i18n.t('metrics.label.maxProfit'), f'{maximum_profit}')
else:
    col3.metric(i18n.t('metrics.label.maxProfit'), f'{maximum_profit}', f'{maximum_profit/abs(invested_amount):.2%}')
if maximum_loss != 0:
    max_profit_over_max_loss = abs(maximum_profit)/abs(maximum_loss)
    col4.metric(i18n.t('metrics.label.profitOverLoss'), f'{max_profit_over_max_loss:.1f}x', f'{max_profit_over_max_loss:.2%}')
else:
    col4.metric(i18n.t('metrics.label.profitOverLoss'), '0')
