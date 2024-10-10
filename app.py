import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Hello, Streamlit!")
st.write("Welcome to your first Streamlit app.")

st.title("Interactive Chart Example")
df = pd.DataFrame({
    "x": [1, 2, 3, 4, 5],
    "y": [10, 11, 12, 13, 14],
    "category": ['A', 'B', 'A', 'B', 'A']
})

fig = px.scatter(df, x='x', y='y', color='category', title='Sample')
st.plotly_chart(fig)
