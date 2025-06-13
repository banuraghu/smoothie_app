# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie :cup_with_straw:")

cust_name = st.text_input("""Enter your name for the order""")
#st.write("""Your order name is :""",cust_name)
st.write(
  """Choose your **fruits** for custom *smoothies!*
  """
)



cnx = st.connect("snowflake")
session=cnx.session
my_dataframe = session.table('SMOOTHIES.PUBLIC.FRUIT_OPTIONS').select(col('FRUIT_NAME'))


ingredient_list = st.multiselect('Choose upto 5 ingredients from the list:',my_dataframe,max_selections=6)
if ingredient_list:

    ingredient_string=''
    for each_fruit in ingredient_list:
        ingredient_string += each_fruit + ' '
 

    insert_stmt ="""insert into smoothies.public.orders(ingredients,customer_name) 
    values ('"""+ingredient_string+"""','"""+cust_name+"""')"""
    #st.write(insert_stmt)
    
    time_to_insert = st.button('Submit Order')


    if time_to_insert:
        session.sql(insert_stmt).collect()
        st.success(f"Your smoothie is getting ready {cust_name}",icon='👍')
       

    
