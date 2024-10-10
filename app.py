import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Hello, Streamlit!")
st.write("Welcome to your first Streamlit app.")

st.sidebar.title("Data Input Sidebar")
name = st.sidebar.text_input("Enter your name")
age = st.sidebar.number_input("Enter your age", min_value=0, max_value=100, value=25)
color = st.sidebar.color_picker("Pick a color")

if st.sidebar.button("aplicar"):
    st.write(f"Hello, {name}!")
    st.write(f"Your age is {age}")
    st.write(f"Your favorite color is {color}")

st.title("Interactive Chart Example")
df = pd.DataFrame({
    "x": [1, 2, 3, 4, 5],
    "y": [10, 11, 12, 13, 14],
    "category": ['A', 'B', 'A', 'B', 'A']
})

fig = px.line(df, x='x', y='y', color='category', title='Sample')
st.plotly_chart(fig)
