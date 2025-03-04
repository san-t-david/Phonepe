#Libaries Used
from sqlalchemy import create_engine
import pandas as pd
import json
from streamlit_option_menu import option_menu
import streamlit as st
import pymysql
import sqlalchemy
import plotly.express as px
import plotly.graph_objects as go
import time

#Streamlit Page Creation
st.set_page_config(page_title='Phonepe Pulse Data Visualization and Exploration',
                layout='wide',initial_sidebar_state='expanded')
st.title(':violet[&emsp;&emsp;&emsp;:bar_chart:**Phonepe Pulse Data Visualization & Exploration**	:chart_with_upwards_trend:]')
st.subheader(':blue[Domain :] Fintech')
with st.sidebar:
    st.title(':blue[Overview of the Project]')
    st.markdown('''The PhonePe Pulse Data Visualization project involves cloning data from a GitHub repository, using it for visualization to enhance user understanding.
                The required data was fetched using the os library,and stored in a MySQL database using PyMySQL.
                Various options were created for users to select and gain insights from the data.
                The project includes creating a live geo map, analyzing the data, and visualizing based on the user-selected options''')
    st.subheader(':blue[Skill Take Away :]')
    st.markdown(''' Github Cloning, Python, Pandas, MySQL,mysql-connector-python, Streamlit, and Plotly''')

# Creating connection with mysql workbench
my_connection = pymysql.connect(host="127.0.0.1",user="root",password="1234")
mycursor = my_connection.cursor()
engine = create_engine("mysql+pymysql://root:1234@127.0.0.1/phonepe")

#Option menu
selected =option_menu(menu_title=None,
                   options=['Map','Analysis','Visualization','Insights'],
                   icons=['geo-alt','search','file-bar-graph','lightbulb'],
                   orientation='horizontal',
                   menu_icon="cast",
                   default_index=0,)

if selected =='Map':
    col1,col2=st.columns(2)
    with col1:
        type = st.selectbox('',options=['Transactions','Users'],label_visibility='collapsed',
                                          placeholder='Select Transactions or Users',)
    with col2:
        year = st.selectbox('', options=[2018, 2019, 2020, 2021, 2022, 2023, 2024], label_visibility='collapsed',
                                placeholder='Select a Year to view',)
# Geo-grapical view for transactions 
    if type == 'Transactions' and year:
        map_query= f'''SELECT State,SUM(Transaction_count) AS Transactions,SUM(Transaction_amount) AS TotalAmount from phonepe.map_transaction
        where Year={year}
        GROUP BY State;'''
        df = pd.read_sql_query(map_query,my_connection)
        fig = px.choropleth(
                            df,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='State',
                            color="Transactions",
                            title=f'PhonePe Transactions - {year}',
                            color_continuous_scale='Rainbow',
                            width=900, height=800, 
                            hover_name='State')
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)

# Bar Chart - Top payment type
        st.markdown("## :violet[Top Payment Type]")
        col1,col2= st.columns(2)
        with col1:
            pay_year = st.selectbox('', options=[2018, 2019, 2020, 2021, 2022, 2023, 2024], placeholder='Year',
                                label_visibility='collapsed', key='pay_year')
        with col2:
            pay_quarter = st.selectbox('', options=[1, 2, 3, 4], placeholder='Quarter', label_visibility='collapsed',key='pay_quarter')

        payment_type=f'''select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from phonepe.aggregate_transaction 
        where Year= {pay_year} and Quarter = {pay_quarter} group by Transaction_type order by Transaction_type;'''
        top_payment= pd.read_sql_query(payment_type, my_connection)
        fig = px.bar(top_payment,
                     title='Transaction Types vs Total_Transactions',
                     x="Transaction_type",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=False)

# Bar chart-Total transactions - State wise
        st.markdown('### :violet[Select options to explore State-wise trends]')
        col1,col2,col3 =st.columns(3)
        with col1:
            state = st.selectbox('',options=['Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                                    'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                    'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                                    'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                    'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                    'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                    'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                    'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                    'Uttarakhand', 'West Bengal'],placeholder='State',
                                label_visibility='collapsed')
        with col2:
            year = st.selectbox('', options=[2018, 2019, 2020, 2021, 2022, 2023, 2024], placeholder='Year',
                                label_visibility='collapsed')
        with col3:
            quarter = st.selectbox('', options=[1, 2, 3, 4], placeholder='Quarter', label_visibility='collapsed')

        trans_state=f'''select State,Year,Quarter,District,sum(Transaction_count) as Total_count, sum(Transaction_amount) as Total_amount from phonepe.map_transaction 
                         where Year = {year} and Quarter = {quarter} and state = '{state}' group by State, District,Year,Quarter order by State,District;'''
        bar_chart_t_state= pd.read_sql_query(trans_state, my_connection)
        
        fig = px.bar(bar_chart_t_state,
                     title=state,
                     x="District",
                     y="Total_count",
                     orientation='v',
                     color='Total_count',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)   

# Geo-grapical view for User 
    elif type == 'Users' and year:
        map_query= f'''SELECT State,SUM(Registered_Users) AS Registered_Users from phonepe.map_user
        where Year={year}
        GROUP BY State;'''
        df = pd.read_sql_query(map_query,my_connection)
        fig = px.choropleth(
                            df,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='State',
                            color="Registered_Users",
                            title=f'PhonePe India Transactions - {year}',
                            color_continuous_scale='Rainbow',
                            width=900, height=800, 
                            hover_name='State')
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)
# Bar chart-Total users - State wise
        st.markdown('### :violet[Select options to explore State-wise trends]')
        col1,col2,col3 =st.columns(3)
        with col1:
            state = st.selectbox('',options=['Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                                    'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                    'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                                    'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                    'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                    'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                    'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                    'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                    'Uttarakhand', 'West Bengal'],placeholder='State',
                                label_visibility='collapsed')
        with col2:
            year = st.selectbox('', options=[2018, 2019, 2020, 2021, 2022, 2023, 2024], placeholder='Year',
                                label_visibility='collapsed')
        with col3:
            quarter = st.selectbox('', options=[1, 2, 3, 4], placeholder='Quarter', label_visibility='collapsed')
            
        
        user_state=f'''select State,Year,Quarter,District,sum(Registered_Users) as Total_Users, sum(App_Opens) as Total_App_Opens from phonepe.map_user 
                         where Year = {year} and Quarter = {quarter} and state = '{state}' group by State, District,Year,Quarter order by State,District;'''
        
        bar_chart_state= pd.read_sql_query(user_state, my_connection)
        
        fig = px.bar(bar_chart_state,
                     title=state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)

# Dashboard for Analysis
elif selected == 'Analysis':
    st.subheader(':orange[Explore Data]')
    col1,col2,col3 =st.columns(3)
    with col1:
        details = st.selectbox('', options=['Transactions', 'Users'], index=None, placeholder='Type',
                                label_visibility='collapsed')
    with col2:
        year = st.selectbox('', options=[2018, 2019, 2020, 2021, 2022, 2023, 2024], placeholder='Year',
                            label_visibility='collapsed')
    with col3:
        quarter = st.selectbox('', options=[1, 2, 3, 4], placeholder='Quarter', label_visibility='collapsed')

#  Transactions overview
    if details == 'Transactions':
        tab1,tab2,tab3=st.tabs(['Transaction Details', 'Categories', 'Top 10'])
        with tab1:
            st.markdown(f':blue[PhonePe Pulse in Q{quarter} - {year}]')
            col1,col2,col3=st.columns(3)
            with col1:
                query1 =f'''SELECT SUM(Transaction_count) AS "All PhonePe Transactions" from phonepe.aggregate_transaction
                where Year={year} and Quarter={quarter};'''
                all_trans= pd.read_sql_query(query1,my_connection)
                st.dataframe(all_trans, hide_index=True)
            with col2:
                query2 = f'''SELECT CONCAT('₹ ',ROUND(SUM(Transaction_amount)/10000000,0),' Cr') AS "Total Payment Value" from phonepe.aggregate_transaction
                where Year={year} and Quarter={quarter};'''
                trans_value = pd.read_sql_query(query2,my_connection)
                st.dataframe(trans_value, hide_index=True)
            with col3:
                query3 = f'''SELECT CONCAT('₹ ',ROUND(SUM(Transaction_Amount)/SUM(Transaction_Count),0)) AS "Average Transaction Value" from phonepe.aggregate_transaction
                where Year={year} and Quarter={quarter};'''
                avg_value = pd.read_sql_query(query3,my_connection)
                st.dataframe(avg_value, hide_index=True)
# Transactions Category-wise split
        with tab2:
            col1,col2 = st.columns(2)
            with col1:
                st.write(f':blue[Transaction Count by Category in Q{quarter} - {year}]')
                query4=f''' SELECT Transaction_type AS Categories, ROUND(SUM(Transaction_count),0) AS "Transaction Count" from phonepe.aggregate_transaction
                where Year={year} and Quarter={quarter} GROUP BY Transaction_type;'''
                category=pd.read_sql_query(query4,my_connection)
                st.dataframe(category,hide_index=True)
            with col2:
                st.write(f':blue[Transaction Amount by Category in Q{quarter} - {year}]')
                query5=f'''SELECT Transaction_type AS Categories, CONCAT('₹ ',ROUND(SUM(Transaction_amount)/10000000,0),' Cr') AS "Transaction Amount" from phonepe.aggregate_transaction
                where Year={year} and Quarter={quarter} GROUP BY Transaction_type;'''
                category_amount=pd.read_sql_query(query5,my_connection)
                st.dataframe(category_amount,hide_index=True)
# Total Transactions: Top-10 State,District,Postalcodes
        with tab3:
            select = st.selectbox('Select Option To View TOP 10 Tables:', options=['Number Of Transactions', 'Total Transaction Amount'])
            if select == "Number Of Transactions":  
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f':blue[Top 10 States in Q{quarter} - {year}]')
                    query6=f'''SELECT DENSE_RANK()OVER(ORDER BY SUM(Transaction_count) DESC) AS RK, State,CONCAT(ROUND(SUM(Transaction_count)/10000000,2),' Cr') AS "Transaction Count" from phonepe.aggregate_transaction 
                    WHERE Year={year} and Quarter={quarter} GROUP BY State ORDER BY RK ASC LIMIT 10;'''
                    top_state = pd.read_sql_query(query6, my_connection)
                    top_state = top_state.drop(columns=['RK'])
                    st.dataframe(top_state, hide_index=True)
                with col2:
                    st.write(f':blue[Top 10 Districts in Q{quarter} - {year}]')
                    query7=f'''SELECT DENSE_RANK()OVER(ORDER BY SUM(Transaction_count) DESC) AS RK, District,CONCAT(ROUND(SUM(Transaction_count)/10000000,2),' Cr') AS "Transaction Count" from phonepe.map_transaction 
                    WHERE Year={year} and Quarter={quarter} GROUP BY District ORDER BY RK ASC LIMIT 10;'''
                    top_district = pd.read_sql_query(query7, my_connection)
                    top_district = top_district.drop(columns=['RK'])
                    st.dataframe(top_district, hide_index=True)
                with col3:
                    st.write(f':blue[Top 10 Postal Codes in Q{quarter} - {year}]')
                    query8=f'''SELECT DENSE_RANK()OVER(ORDER BY SUM(Transaction_count) DESC) AS RK, Pincodes,CONCAT(ROUND(SUM(Transaction_count)/10000000,2),' Cr') AS "Transaction Count" from phonepe.top_transaction 
                    WHERE Year={year} and Quarter={quarter} GROUP BY Pincodes ORDER BY RK ASC LIMIT 10;'''
                    top_pincode = pd.read_sql_query(query8, my_connection)
                    top_pincode = top_pincode.drop(columns=['RK'])
                    st.dataframe(top_pincode,column_config={'Pincodes':'Postal Codes'}, hide_index=True)

# Total Transaction Amount: Top-10 State,District,Postalcodes
            if select == "Total Transaction Amount":
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f':blue[Top 10 States in Q{quarter} - {year}]')
                    query6=f'''SELECT DENSE_RANK()OVER(ORDER BY SUM(Transaction_count) DESC) AS RK, State,CONCAT('₹ ',ROUND(SUM(Transaction_amount)/10000000,0),' Cr') AS "Transaction Amount" from phonepe.aggregate_transaction 
                    WHERE Year={year} and Quarter={quarter} GROUP BY State ORDER BY RK ASC LIMIT 10;'''
                    top_state = pd.read_sql_query(query6, my_connection)
                    top_state = top_state.drop(columns=['RK'])
                    st.dataframe(top_state, hide_index=True)
                with col2:
                    st.write(f':blue[Top 10 Districts in Q{quarter} - {year}]')
                    query7=f'''SELECT DENSE_RANK()OVER(ORDER BY SUM(Transaction_count) DESC) AS RK, District,CONCAT('₹ ',ROUND(SUM(Transaction_amount)/10000000,0),' Cr') AS "Transaction Amount" from phonepe.map_transaction 
                    WHERE Year={year} and Quarter={quarter} GROUP BY District ORDER BY RK ASC LIMIT 10;'''
                    top_district = pd.read_sql_query(query7, my_connection)
                    top_district = top_district.drop(columns=['RK'])
                    st.dataframe(top_district, hide_index=True)
                with col3:
                    st.write(f':blue[Top 10 Postal Codes in Q{quarter} - {year}]')
                    query8=f'''SELECT DENSE_RANK()OVER(ORDER BY SUM(Transaction_count) DESC) AS RK, Pincodes,CONCAT('₹ ',ROUND(SUM(Transaction_amount)/10000000,0),' Cr') AS "Transaction Amount" from phonepe.top_transaction 
                    WHERE Year={year} and Quarter={quarter} GROUP BY Pincodes ORDER BY RK ASC LIMIT 10;'''
                    top_pincode = pd.read_sql_query(query8, my_connection)
                    top_pincode = top_pincode.drop(columns=['RK'])
                    st.dataframe(top_pincode,column_config={'Pincodes':'Postal Codes'}, hide_index=True)
#  Users overview
    elif details == 'Users':
        tab1,tab2=st.tabs(['User Details', 'Top 10 Users'])
        with tab1:
            col1,col2=st.columns(2)
            with col1:
                st.write(f':blue[Registered PhonePe Users till Q{quarter} - {year}]')
                query9 =f'''SELECT SUM(User_count) AS "Total Number of Users" from phonepe.aggregate_user
                where Year={year} and Quarter={quarter};'''
                all_users= pd.read_sql_query(query9,my_connection)
                st.dataframe(all_users, hide_index=True)
            with col2:
                st.write(f':blue[PhonePe app opens in Q{quarter} - {year}]')
                query10 = f'''SELECT CASE WHEN SUM(App_Opens)=0 THEN 'Unavailable' ELSE SUM(App_Opens) END AS "App Opens" from phonepe.map_user
                where Year={year} and Quarter={quarter};'''
                app_opens = pd.read_sql_query(query10,my_connection)
                st.dataframe(app_opens, hide_index=True)
#  Users: Top-10 State,District,Postalcodes
        with tab2: 
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f':blue[Top 10 States in Q{quarter} - {year}]')
                query11=f'''SELECT DENSE_RANK()OVER(ORDER BY SUM(User_count) DESC) AS RK, State,SUM(User_count) AS "User Count" from phonepe.aggregate_user 
                WHERE Year={year} and Quarter={quarter} GROUP BY State ORDER BY RK ASC LIMIT 10;'''
                top_state = pd.read_sql_query(query11, my_connection)
                top_state = top_state.drop(columns=['RK'])
                st.dataframe(top_state, hide_index=True)
            with col2:
                st.write(f':blue[Top 10 District in Q{quarter} - {year}]')
                query12=f'''SELECT DENSE_RANK()OVER(ORDER BY SUM(Registered_Users) DESC) AS RK, District,SUM(Registered_Users) AS "Registered Users" from phonepe.map_user 
                WHERE Year={year} and Quarter={quarter} GROUP BY District ORDER BY RK ASC LIMIT 10;'''
                top_district = pd.read_sql_query(query12, my_connection)
                top_district = top_district.drop(columns=['RK'])
                st.dataframe(top_district, hide_index=True)
            with col3:
                st.write(f':blue[Top 10 Postal code in Q{quarter} - {year}]')
                query13=f'''SELECT DENSE_RANK()OVER(ORDER BY SUM(Registered_Users) DESC) AS RK, Pincodes,SUM(Registered_Users) AS "Registered Users" from phonepe.top_user 
                WHERE Year={year} and Quarter={quarter} GROUP BY Pincodes ORDER BY RK ASC LIMIT 10;'''
                top_pincode = pd.read_sql_query(query13, my_connection)
                top_pincode = top_pincode.drop(columns=['RK'])
                st.dataframe(top_pincode,column_config={'Pincodes':'Postal Code'}, hide_index=True)
# Visualization
elif selected == 'Visualization':
    st.subheader(':orange[Explore Data]')
    col1,col2,col3 =st.columns(3)
    with col1:
        details = st.selectbox('', options=['Transactions', 'Users'], index=None, placeholder='Type',
                                label_visibility='collapsed')
    with col2:
        year = st.selectbox('', options=[2018, 2019, 2020, 2021, 2022, 2023, 2024], placeholder='Year',
                            label_visibility='collapsed')
    with col3:
        quarter = st.selectbox('', options=[1, 2, 3, 4], placeholder='Quarter', label_visibility='collapsed')

    if details == 'Transactions':
        tab1, tab2, tab3 = st.tabs(["States", "Districts", "Postal Codes"])
        with tab1:
            st.markdown("### :violet[States]")
            query14=f'''SELECT State, SUM(Transaction_count) as Total_Transactions_Count, SUM(Transaction_amount) as Total_Transaction_Amount from phonepe.aggregate_transaction 
            where Year = {year} and Quarter = {quarter} group by State order by Total_Transaction_Amount desc limit 10;'''
            top10_state= pd.read_sql_query(query14, my_connection)
            fig = px.pie(top10_state, values='Total_Transaction_Amount',
                            names='State',
                            title='Top 10 State based on Total number of transaction and Total amount',width=1000,height=600,
                            color_discrete_sequence=px.colors.sequential.Viridis,
                            hover_data=['Total_Transactions_Count'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
        with tab2:
            st.markdown("### :violet[Districts]")
            query15=f'''select District , SUM(Transaction_count) as Total_Count, SUM(Transaction_amount) as Total_Amount from phonepe.map_transaction 
            where Year = {year} and Quarter = {quarter} group by District order by Total_Amount desc limit 10;'''
            top10_district= pd.read_sql_query(query15, my_connection)
            fig = px.pie(top10_district, values='Total_Amount',
                            names='District',width=1000,height=600,
                            title='Top 10 District based on Total number of transaction and Total amount',
                            color_discrete_sequence=px.colors.sequential.Agsunset,
                            hover_data=['Total_Count'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
        with tab3:
            st.markdown("### :violet[Postal Codes]")
            query16=f'''select Pincodes, sum(Transaction_count) as Total_Transaction_Count, sum(Transaction_amount) as Total_Transaction_Amount from phonepe.top_transaction 
                            where Year = {year} and Quarter = {quarter} group by Pincodes order by Total_Transaction_Amount desc limit 10;'''
            top10_postalcodes= pd.read_sql_query(query16, my_connection)
            fig = px.pie(top10_postalcodes, values='Total_Transaction_Amount',
                            names='Pincodes',width=1000,height=600,
                            title='Top 10 Pincode based on Total number of transaction and Total amount',
                            color_discrete_sequence=px.colors.sequential.Blugrn,
                            hover_data=['Total_Transaction_Count'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
    
    elif details == 'Users':
        tab1,tab2,tab3 = st.tabs(["Brands", "Districts","States"])
        with tab1:
            st.markdown("### :violet[Brands]")
            query17=f'''select User_Brands, sum(User_count) as Total_Users, avg(User_Percentage)*100 as Avg_Percentage from phonepe.aggregate_user 
            where Year = {year} and Quarter = {quarter} group by User_Brands order by Total_Users desc limit 10;'''
            top10_mobile_brands= pd.read_sql_query(query17, my_connection)
            fig = px.bar(top10_mobile_brands,
                            title='Top 10 Mobile Brands and Percentage',
                            y="Total_Users",
                            x="User_Brands",
                            color='Avg_Percentage',
                            color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)
        with tab2:
            st.markdown("### :violet[Districts]")
            query18=f'''select District, sum(Registered_Users) as Total_Users, sum(App_Opens) as Total_App_Opens from phonepe.map_user 
            where Year = {year} and Quarter = {quarter} group by District order by Total_Users desc limit 10;'''
            top10_user_districts= pd.read_sql_query(query18, my_connection)
            fig = px.bar(top10_user_districts,
                        title='Top 10 District based on Total app opens frequency by users',
                        y="Total_Users",
                        x="District",
                        color='Total_Users',
                        color_continuous_scale=px.colors.sequential.Tealgrn)
            st.plotly_chart(fig,use_container_width=True)
        with tab3:
            st.markdown("### :violet[States]")
            query19=f'''select State, sum(Registered_Users) as Total_Users, sum(App_Opens) as Total_App_Opens from phonepe.map_user 
            where Year = {year} and Quarter = {quarter} group by State order by Total_Users desc limit 10;'''
            top10_user_postalcodes= pd.read_sql_query(query19, my_connection)
            fig = px.bar(top10_user_postalcodes,
                        title='Top 10 States by users',
                        y='Total_Users',
                        x='State',
                        color='Total_Users', 
                        color_continuous_scale=px.colors.sequential.Aggrnyl)
            st.plotly_chart(fig, use_container_width=True)

elif selected == 'Insights':
    st.markdown(':blue[Select the fact you want to see]')
    facts= st.selectbox('',['Top States by Total Transaction Count',
                            'Top Districts by Total Transaction Amount',
                            'Top States by Total Transaction Amount',
                            'Year-wise Total Transactions',
                            'Top States by Total Users',
                            'Top Mobile Brands by User Count',
                            'Top Districts by Total Users',
                            'States with the Fewest Transactions',
                            'Top Pincodes by Total Transactions',
                            'Top Pincodes by Total Users'])
    def stream_text(text):
        for char in text:
            yield char
            time.sleep(0.02)

    if facts == 'Top States by Total Transaction Count':
        col1, col2 = st.columns([2,1])

        with col1:
            query20=f'''SELECT State, SUM(Transaction_count) AS Total_Transaction_Count FROM phonepe.aggregate_transaction
                    GROUP BY State ORDER BY Total_Transaction_Count DESC LIMIT 10;'''
            top10_states_transaction_count= pd.read_sql_query(query20, my_connection)
            fig = px.bar(top10_states_transaction_count,
                            title='Top 10 States by Total Transaction Count',
                            y='Total_Transaction_Count',
                            x='State',
                            color='Total_Transaction_Count',
                            color_continuous_scale=px.colors.sequential.Aggrnyl,
                            hover_data={'Total_Transaction_Count': True, 'State': False})
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            for _ in range(10):
                st.write('')
            
            detailed_descriptions = [
                '''Maharashtra leads with a transaction volume of Rs.2200 Cr, indicating a high adoption rate of digital payments. 
                Karnataka and Telangana are growing rapidly, while Madhya Pradesh shows potential for expansion.''']
            
            for description in detailed_descriptions:
                st.write_stream(stream_text(description))
    
    if facts == 'Top States by Total Transaction Amount':
        col1, col2 = st.columns([2,1])
        with col1:
            query21=f'''SELECT State, ROUND(SUM(Transaction_amount)/10000000,2) AS Total_Transaction_Amount FROM phonepe.aggregate_transaction
                    GROUP BY State ORDER BY Total_Transaction_Amount DESC LIMIT 10;'''
            top10_states_transaction_amount= pd.read_sql_query(query21, my_connection)
            fig = px.bar(top10_states_transaction_amount,
                            title='Top 10 States by Total Transaction Amount',
                            y='Total_Transaction_Amount',
                            x='State',
                            color='Total_Transaction_Amount',
                            color_continuous_scale='viridis',
                            hover_data={'Total_Transaction_Amount': True, 'State': False})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            for _ in range(10):
                st.write('')
            
            detailed_descriptions = [
                '''Telangana tops the list with the highest transaction amount, followed by Maharashtra and Karnataka. 
                Andhra Pradesh and Rajasthan also show strong digital payment activity, while Uttar Pradesh and Madhya Pradesh are emerging contenders. 
                Bihar and West Bengal have notable transaction volumes, and Tamil Nadu completes the top 10.''']
            
            for description in detailed_descriptions:
                st.write_stream(stream_text(description))

    if facts == 'Top States by Total Users':
        col1, col2 = st.columns([2,1])
        with col1:
            query22=f'''select State, sum(Registered_Users) as Total_Users, sum(App_Opens) as Total_App_Opens from phonepe.map_user 
             group by State order by Total_Users desc limit 10;'''
            top_states_total_users= pd.read_sql_query(query22, my_connection)
            fig = px.bar(top_states_total_users,
                        title='Top 10 States by users',
                        y='Total_Users',
                        x='State',
                        color='Total_Users', 
                        color_continuous_scale=px.colors.sequential.Aggrnyl,
                        hover_data={'Total_Users': True, 'State': False})
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            for _ in range(10):
                st.write('')
            
            detailed_descriptions = [
                '''Maharashtra has the highest user count, followed closely by Uttar Pradesh. 
                Karnataka, Andhra Pradesh, and Rajasthan round out the top five states in terms of total users. 
                Gujarat, despite being a major state, has the lowest user count among the listed states, suggesting potential for user base expansion.''']
            
            for description in detailed_descriptions:
                st.write_stream(stream_text(description))
    
    if facts == 'Top Mobile Brands by User Count':
        col1, col2 = st.columns([2,1])
        with col1:
            query23=f'''select User_Brands, sum(User_count) as Total_Users, avg(User_Percentage)*100 as Avg_Percentage from phonepe.aggregate_user 
                    group by User_Brands order by Total_Users desc limit 10;'''
            top10_mobile_brands= pd.read_sql_query(query23, my_connection)
            fig = px.bar(top10_mobile_brands,
                            title='Top 10 Mobile Brands and Percentage',
                            y="Total_Users",
                            x="User_Brands",
                            color='Avg_Percentage',
                            color_continuous_scale=px.colors.sequential.Agsunset,
                            hover_data={'Total_Users': True, 'User_Brands': False})
            st.plotly_chart(fig,use_container_width=True)

        with col2:
            for _ in range(10):
                st.write('')
            
            detailed_descriptions = [
                '''Xiaomi dominates with over 26% of Total users, followed by Samsung and Vivo. 
                Mid-range brands like Realme and Oppo have significant users, while premium brands like Apple and OnePlus have smaller but notable users.''']
            
            for description in detailed_descriptions:
                st.write_stream(stream_text(description))

    if facts == 'Top Districts by Total Transaction Amount':
        col1, col2 = st.columns([2,1])
        with col1:
            query24=f'''select District, ROUND(SUM(Transaction_amount)/10000000,2) as Total_Transaction_Amount from phonepe.map_transaction
                        group by District order by Total_Transaction_Amount desc limit 10;'''
            top10_districts_transaction_amount= pd.read_sql_query(query24, my_connection)
            fig = px.bar(top10_districts_transaction_amount,
                            title='Top 10 Districts by Total Transaction Amount',
                            y='Total_Transaction_Amount',
                            x='District',
                            color='Total_Transaction_Amount',
                            color_continuous_scale='viridis',
                            hover_data={'Total_Transaction_Amount': True, 'District': False})
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            for _ in range(10):
                st.write('')
            
            detailed_descriptions = [
                '''Bengaluru Urban District leads with the highest total amount of ₹1,477,074 crore, followed by Hyderabad District at ₹1,018,401 crore. 
                Pune District ranks third with ₹744,880.8 crore, while Jaipur and Rangareddy districts round out the top five with ₹635,222.2 crore and ₹493,405.4 crore respectively. 
                The data suggests a concentration of economic activity in major urban and tech hubs across different states in India.''']
            
            for description in detailed_descriptions:
                st.write_stream(stream_text(description))

    if facts ==  'Top Districts by Total Users':
        col1, col2 = st.columns([2,1])
        with col1:
            query25=f'''select District, sum(Registered_Users) as Total_Users from phonepe.map_user
                        group by District order by Total_Users desc limit 10;'''
            top10_districts_total_users= pd.read_sql_query(query25, my_connection)
            fig = px.bar(top10_districts_total_users,
                            title='Top 10 Districts by Total Users',
                            y='Total_Users',
                            x='District',
                            color='Total_Users',
                            color_continuous_scale='viridis',
                            hover_data={'Total_Users': True, 'District': False})
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            for _ in range(10):
                st.write('')
            
            detailed_descriptions = [
                '''Bengaluru Urban District leads with 250 million users, significantly ahead of Pune District's 162 million. 
                Jaipur and Thane districts follow closely, each with around 100 million users. Mumbai Suburban District ranks fifth with 98.1 million users, 
                while Hyderabad and Ahmadabad districts have 84 million and 76 million users respectively, showcasing a concentration of digital adoption in major urban centers across India.''']
            
            for description in detailed_descriptions:
                st.write_stream(stream_text(description))

    if facts == 'Year-wise Total Transactions':
        col1, col2 = st.columns([2,1])
        with col1:
            query26=f'''SELECT Year, ROUND(SUM(Transaction_amount)/10000000,2) AS Total_Transaction_Amount FROM phonepe.aggregate_transaction
                    GROUP BY Year ORDER BY Year DESC;;'''
            year_wise_total_transaction_amount= pd.read_sql_query(query26, my_connection)
            fig = px.bar(year_wise_total_transaction_amount,
                            title='Year-wise Total Transactions',
                            y='Total_Transaction_Amount',
                            x='Year',
                            color='Total_Transaction_Amount',
                            color_continuous_scale='viridis',
                            hover_data={'Total_Transaction_Amount': True, 'Year': False})
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            for _ in range(10):
                st.write('')
            
            detailed_descriptions = [
                '''The total amount has grown exponentially from ₹162,304.5 crores in 2018 to ₹9,449,181 crores in 2023, showing rapid digital payment adoption. 
                2023 marked the peak year with ₹9,449,181 crores, nearly 1.5 times the amount in 2022 (₹6,426,633 crores). 
                The data for 2024 (₹2,945,843 crores) is partial, likely representing only the first quarter, indicating continued strong growth in digital transactions.''']
            
            for description in detailed_descriptions:
                st.write_stream(stream_text(description))

    if facts == 'States with the Fewest Transactions':
        col1, col2 = st.columns([2,1])
        with col1:
            query27=f'''SELECT State, SUM(Transaction_count) AS Total_Transaction_Count FROM phonepe.aggregate_transaction
                        GROUP BY State ORDER BY Total_Transaction_Count ASC LIMIT 10;'''
            states_with_the_fewest_transactions= pd.read_sql_query(query27, my_connection)
            fig = px.bar(states_with_the_fewest_transactions,
                            title='States with the Fewest Transactions',
                            y='Total_Transaction_Count',
                            x='State',
                            color='Total_Transaction_Count',
                            color_continuous_scale='viridis',
                            hover_data={'Total_Transaction_Count': True, 'State': False})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            for _ in range(10):
                st.write('')
            
            detailed_descriptions = [
                '''Lakshadweep has the lowest count at 419,654 transactions, while Mizoram and Ladakh follow with 12.5 million and 21.4 million respectively. 
                The data shows significant variation in digital transaction adoption among smaller states and union territories, 
                with northeastern states generally showing higher transaction counts.''']
            
            for description in detailed_descriptions:
                st.write_stream(stream_text(description))

    if facts == 'Top Pincodes by Total Transactions':
        col1, col2 = st.columns([2,1])
        with col1:
            query28=f'''SELECT Pincodes, ROUND(SUM(Transaction_count)/10000000,2)  AS Total_Transaction_Count FROM phonepe.top_transaction
                        GROUP BY Pincodes ORDER BY Total_Transaction_Count DESC LIMIT 10;'''
            top_pincodes_by_total_transactions= pd.read_sql_query(query28, my_connection)
            fig = px.pie(top_pincodes_by_total_transactions,
                        names='Pincodes',
                        values='Total_Transaction_Count',
                        title='Top Pincodes by Total Transactions',
                        color_discrete_sequence=px.colors.sequential.Viridis,
                        hover_data={'Total_Transaction_Count': True, 'Pincodes': False})

            fig.update_traces(textposition='inside', textinfo='label')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            for _ in range(10):
                st.write('')
            
            detailed_descriptions = [
                '''Banjara Hills (Hyderabad) - 500034 leads with 179.98 crore transactions, followed by Bangalore G P O (Bangalore)-560001 with 150.86 crore and Hyderabad G.P.O. (Hyderbad)-500001 with 147.38 crore. 
                The top three pincodes, all exceeding 147 crore transactions, likely represent major urban or commercial centers. 
                There's a significant drop after the top 5, with the 6th pincode (302016) having 85.65 crore transactions, suggesting a concentration of high transaction volumes in a few key areas.''']
            
            for description in detailed_descriptions:
                st.write_stream(stream_text(description))

    if facts == 'Top Pincodes by Total Users':
        col1, col2 = st.columns([2,1])
        with col1:
            query29=f'''SELECT Pincodes, (SUM(Registered_Users)/10000000)  AS Total_User_Count FROM phonepe.top_user
                        GROUP BY Pincodes ORDER BY Total_User_Count DESC LIMIT 10;'''
            top_pincodes_by_total_users= pd.read_sql_query(query29, my_connection)
            fig = px.pie(top_pincodes_by_total_users,
                        names='Pincodes',
                        values='Total_User_Count',
                        title='Top Pincodes by Total Users',
                        color_discrete_sequence=px.colors.sequential.Viridis,
                        hover_data={'Total_User_Count': True, 'Pincodes': False})
            fig.update_traces(textposition='inside', textinfo='label')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            for _ in range(10):
                st.write('')
            
            detailed_descriptions = [
                '''Gautam Buddha Nagar (Noida)-201301 leads with 1.3961 crore users, followed by Uttam Nagar (West Delhi)-110059 with 1.1671 crore and Bommanahalli (Bangalore)-560068 with 1.0913 crore users. 
                The top three pincodes are the only ones with over 1 crore users each, indicating concentrated user bases in these areas. 
                There's a gradual decrease in user count from the 4th to 10th pincode, ranging from 0.9877 crore to 0.7695 crore users, suggesting a more evenly distributed user base among these areas.''']
            
            for description in detailed_descriptions:
                st.write_stream(stream_text(description))
    


        


    



                

