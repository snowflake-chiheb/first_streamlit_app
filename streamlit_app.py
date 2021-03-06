
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
def get_fruit_data(fruit):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
    # load the data into a dataframe 
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

try:
  fruit_choice = st.text_input('What fruit would you like information about?')
  if not fruit_choice:
    st.error('Please select a fruit to get informations.')
    
  else:
    fruityvice_normalized = get_fruit_data(fruit_choice)
    # ddissplay the dataframe in table format using sstreamlit
    st.dataframe(fruityvice_normalized)
    
 
except URLError as e:
  st.error()


def load_fruit_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()
def insert_fruit(fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute(f"insert into  fruit_load_list values ('{fruit}') ")
        return 'Thanks for adding ' + fruit

        
st.header("View Our Fruit List - Add your Favorites !")

if st.button('Get fruit load list'):
    # Snowflake connection 
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    my_data_row = load_fruit_list()
    my_cnx.close()
    st.dataframe(my_data_row)
fruit_2_add = st.text_input('What fruit would you like to add  ?')
if st.button('Add fruit to list'):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    function_log = insert_fruit(fruit_2_add)
    my_cnx.close()
    st.write(function_log)



