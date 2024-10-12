import numpy as np
import streamlit as st
import plotly.graph_objects as go

from opcoes.opcao import Call, Put

# st.session_state.show_graphic = False
# st.markdown("<h1 style='text-align: center;'>Gráfico Interativo</h1>", unsafe_allow_html=True)
st.title("Gráfico Interativo")
adicionar = st.button("Adicionar Opção")

@st.dialog("Adicione uma opção")
def adicionar_opcao():
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
    quantidade = st.number_input('Quantidade: ', min_value=1, step=100, value=100)
    submitted = st.button("Adicionar")
    if submitted:
        st.session_state.opcao_info = {
            'opcao': Call(strike, premio) if tipo_opcao == 'Call' else Put(strike, premio),
            'strike': strike, 
            'premio': premio,
            'tipo_opcao': tipo_opcao,
            'operacao': operacao, 
            'quantidade': quantidade
        }
        st.session_state.show_graphic = True
        st.rerun()

if adicionar:
    adicionar_opcao()

# if st.session_state.show_graphic == True:
fig = go.Figure()
opcao = st.session_state.opcao_info
x = np.arange(opcao['strike'] - 2, 14, 0.01)
y = opcao['opcao'].calcular_payoff(x)
fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Line Plot'))

fig.update_layout(
    title={
        'text': 'Resultado no Vencimento',
        'x': 0.55,
        'xanchor': 'center'
    },
    xaxis_title='Preço do Ativo (R$)',
    yaxis_title='Lucro/Prejuízo (R$)',
    width=800,
    height=600,
    template='plotly_dark'
)

st.plotly_chart(fig)



# col1, col2 = st.columns([1, 2])
# with col1:
#     with st.form("opcao"):
#         tipo_opcao = st.radio(
#             'Tipo de opção:',
#             ['Call', 'Put'],
#             captions=['Opção de Compra', 'Opção de Venda']
#         )
#         operacao = st.radio(
#             'Tipo de operação:',
#             ['Compra', 'Venda'],
#             captions=['Compra de Opção', 'Venda de Opção']
#         )
#         strike = st.number_input('Strike: ', min_value=0.01, step=0.01)
#         premio = st.number_input('Prêmio: ', min_value=0.01, step=0.01)
#         quantidade = st.number_input('Quantidade: ', min_value=1, step=100, value=100)
#         submitted = st.form_submit_button("Adicionar")
#         if submitted:
#             st.session_state.opcao_info = {
#                 'opcao': Call(strike, premio) if tipo_opcao == 'Call' else Put(strike, premio),
#                 'strike': strike, 
#                 'premio': premio,
#                 'tipo_opcao': tipo_opcao,
#                 'operacao': operacao, 
#                 'quantidade': quantidade
#             }
# with col2:
#     if submitted:
#         fig = go.Figure()
#         x = np.arange(strike - 2, 14, 0.01)
#         y = st.session_state.opcao_info['opcao'].calcular_payoff(x)
#         fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Line Plot'))

#         fig.update_layout(
#             title={
#                 'text': 'Resultado no Vencimento',
#                 'x': 0.55,
#                 'xanchor': 'center'
#             },
#             xaxis_title='Preço do Ativo (R$)',
#             yaxis_title='Lucro/Prejuízo (R$)',
#             width=800,
#             height=600,
#             template='plotly_dark'
#         )

#         st.plotly_chart(fig)
# with col3:
#     st.header("Column 3")
#     st.write("Content 3")