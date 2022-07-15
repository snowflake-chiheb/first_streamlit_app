
import streamlit as st
import pandas as pd 

st.title('My Parents New Healthy Dinner')
st.header('Breakfast Menu')
st.text('🥣  Omega 3 & Blueberry otmeal')
st.text('🥗 Kale, Spinach, Rocker smoothie')
st.text('🐔 Hard-boiled Freee Range Egg')
st.text('🥑🍞 Avocado Toast')
st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
st.dataframe(my_fruit_list)
