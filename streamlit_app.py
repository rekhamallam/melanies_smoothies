
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
#smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
# Write directly to the app
st.title(f"🥤 Customize Your Smoothie 🥤 {st.__version__}")
st.write(
    """ Choose any 5 fruits!
    """
)
name_on_order = st.text_input("Name on Order", "adya")
st.write("The currentName of Order is", name_on_order)
cnx = st.connection("snowflake")
#session = get_active_session()
session = cnx.session()
#my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()

# Display the dataframe
st.dataframe(pd_df)
st.stop()
# Extract the value from each Row object into a simple Python list
ingredients_list = st.multiselect(
    'Choose any 5 fruits:'
    , my_dataframe
    , max_selections =5
    ) 

if ingredients_list:
        ingredients_string = ''
    
        for FRUIT_CHOSEN in ingredients_list:
            ingredients_string += FRUIT_CHOSEN + ' '

            search_on=pd_df.loc[pd_df['FRUI_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
            st.write('he search value for' , FRUIT_CHOSEN,' is ', search_on, '.')
        st.subheader(FRUIT_CHOSEN + 'Nutrition Information')
        #sf_df = st.dataframe(data=smothieifroot_response.json(), use_container_width=True)
        
        my_insert_stmt = """ insert into smoothies.public.orders(INGREDIENTS,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """');"""
        st.write(my_insert_stmt)
        time_to_insert = st.button ('submit order')

        if(time_to_insert):
            session.sql(my_insert_stmt).collect()
            st.success('your order is placed')
            
            smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + FRUIT_CHOSEN)
            sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)


        
        

