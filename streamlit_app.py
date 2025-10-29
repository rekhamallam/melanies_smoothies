
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)


# Write directly to the app
st.title(f"🥤 Customize Your Smoothie 🥤 {st.__version__}")
st.write(
    """ Choose any 5 fruits!
    """
)

name_on_order = st.text_input("Name on Order", "Mellymel")
st.write("The currentName of Order is", name_on_order)

cnx = st.connection("snowflake")
#session = get_active_session()
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Extract the value from each Row object into a simple Python list
ingredients_list = st.multiselect('Choose any 5 fruits!',my_dataframe, max_selections =5) 
st.write(ingredients_list)

if ingredients_list:
    
    
    ingredients_string = ''
    for FRUIT_NAME in ingredients_list:
        ingredients_list += FRUIT_NAME + ' '
        st.subheader(FRUIT_NAME + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://mysmoothiefroot.com/api/fruit" + fruit_chosen)
        sf_df =st.dataframe(data=smothieifroot_response.json(), use_container_width=True)
    my_insert_stmt = """ insert into smoothies.public.orders(INGREDIENTS,name_on_order)
    values ('""" + ingredients_list + """','""" + name_on_order + """');"""
    st.write(my_insert_stmt)
    time_to_insert = st.button ('submit order')

    if(time_to_insert):
            session.sql(my_insert_stmt).collect()
            st.success('your order is placed')

        
        

