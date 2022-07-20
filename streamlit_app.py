
import streamlit as st
import pandas as pd 
import requests
import snowflake.connector 
from urllib.error import URLError

st.title('My Parents New Healthy Dinner')
st.header('Breakfast Menu')
st.text('🥣  Omega 3 & Blueberry otmeal')
st.text('🥗 Kale, Spinach, Rocker smoothie')
st.text('🐔 Hard-boiled Freee Range Egg')
st.text('🥑🍞 Avocado Toast')
st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# set the dataframe index to fruit name 
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
# filter the data based on the selector 
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
st.dataframe(fruits_to_show)
# API section 
st.header("Fruityvice Fruit Advice!")
# added an input to chose the fruit
try:
  fruit_choice = st.text_input('What fruit would you like information about?')
  if fruit_choice:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
    # load the data into a dataframe 
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    # ddissplay the dataframe in table format using sstreamlit
    st.dataframe(fruityvice_normalized)
  else:
    st.error('Please select a fruit to get informations.')
 
except URLError as e:
  st.error()

st.stop()
# Snowflake connection 
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchall()
st.header("The  fruit load  list contains :")
st.dataframe(my_data_row)
fruit_2_add = st.text_input('What fruit would you like to add  ?')
st.write('Thanks for adding', fruit_2_add)

my_cur.execute("insert into  fruit_load_list values ('from stremlit') ")
