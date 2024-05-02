# Import python packages
import streamlit as st
import pandas as pd
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customise your Smoothie :cup_with_straw:")
st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)

st.write("Choose the fruits you want in your custom smoothie!")

name_on_order = st.text_input('Name on Smoothie: ')
st.write('The name on your Smoothie will be: ', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections = 5)

if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)

    ingredients_string=''

    for ingredient in ingredients_list:
        ingredients_string+=ingredient + " "
        st.subheader(ingredient + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + ingredient)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(name_on_order, ingredients)
                values ('""" + name_on_order + """','""" + ingredients_string + """')"""
    
    st.write(my_insert_stmt)
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!' , icon="✅")
    

