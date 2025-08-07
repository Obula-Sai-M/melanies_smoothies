# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Set up the page
st.set_page_config(page_title="Custom Smoothie", page_icon="🥤")

# Title
st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom smoothie!")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Example fruit list
fruits = ["Banana", "Strawberries", "Peaches"]

# Dropdown to select a fruit
selected_fruit = st.selectbox(
    label="What is your favorite fruit?",
    options=fruits,
    index=0,
    help="Choose one fruit to add to your smoothie",
    key="fruit_selector",
    placeholder="Select a fruit",
)

# Show selection
st.write(f"Your favorite fruit is: **{selected_fruit}**")


cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)
if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_string + """','""" + name_on_order+ """')"""

    # st.write(my_insert_stmt)
    # st.stop()
    
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

        
