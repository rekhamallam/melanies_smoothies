




# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"🥤 Customize Your Smoothie 🥤 {st.__version__}")
st.write(
    """ Choose any 5 fruits!
    """
)

name_on_order = st.text_input("Name on Order", "Mellymel")
st.write("The currentName of Order is", name_on_order)


session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Extract the value from each Row object into a simple Python list
ingredients_string = st.multiselect('Choose any 5 fruits!',my_dataframe, max_selections =5) 
st.write(ingredients_string)

if ingredients_string:
    
    
    ingredients_list = ''
    for FRUIT_NAME in ingredients_string:
        ingredients_list += FRUIT_NAME + ' '
        

    my_insert_stmt = """ insert into smoothies.public.orders(INGREDIENTS,name_on_order)
    values ('""" + ingredients_list + """','""" + name_on_order + """');"""
    st.write(my_insert_stmt)
    time_to_insert = st.button ('submit order')

    if(time_to_insert):
            session.sql(my_insert_stmt).collect()
            st.success('your order is placed')

        
        

