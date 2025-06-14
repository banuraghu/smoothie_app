# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie :cup_with_straw:")

cust_name = st.text_input("""Enter your name for the order""")
#st.write("""Your order name is :""",cust_name)
st.write(
  """Choose your **fruits** for custom *smoothies!*
  """
)

cnx = st.connection("snowflake")
session=cnx.session()
my_dataframe = session.table('SMOOTHIES.PUBLIC.FRUIT_OPTIONS').select (col('FRUIT_NAME'), col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()


ingredient_list = st.multiselect('Choose upto 5 ingredients from the list:',my_dataframe,max_selections=6)
if ingredient_list:

    ingredient_string=''
    for each_fruit in ingredient_list:
        ingredient_string += each_fruit + ' '
      
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == each_fruit, 'SEARCH_ON'].iloc[0]
        st.subheader(each_fruit + ' Nutrition Information ')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width = True)
        
 

    insert_stmt ="""insert into smoothies.public.orders(ingredients,name_on_order) 
    values ('"""+ingredient_string+"""','"""+cust_name+"""')"""
    #st.write(insert_stmt)
    
    time_to_insert = st.button('Submit Order')


    if time_to_insert:
        session.sql(insert_stmt).collect()
        st.success(f"Your smoothie is getting ready {cust_name}",icon='👍')
       

    
