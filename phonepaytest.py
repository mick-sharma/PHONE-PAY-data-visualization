import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import requests
import json
from PIL import Image



#CREATE DATAFRAMES FROM SQL
#sql connection
hostname='localhost'
database= 'phonepay_pulse'
username= 'postgres'
pwd= 'root'
port_id= 5432


mydb = psycopg2.connect(host = hostname,
                        user = username,
                        password = pwd,
                        database = database,
                        port = port_id
                        )
cursor = mydb.cursor()


#Aggregated_insurance
cursor.execute("select * from aggregated_insurance;")
mydb.commit()
table7 = cursor.fetchall()

Aggre_insurance = pd.DataFrame(table7,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count","Transaction_amount"))

#1. Aggregated_transsaction

cursor.execute(" select * from aggregated_transaction")
mydb.commit()
table1= cursor.fetchall()

Aggre_transaction = pd.DataFrame(table1,columns = ("States","Years","Quarter","Transaction_type","Transaction_count",
                                                    "Transaction_amount"))


#2. Aggregated_user

cursor.execute("select * from aggregated_user ")
mydb.commit()
table2= cursor.fetchall()

Aggre_user = pd.DataFrame(table2, columns = ("States", "Years","Quarter","Brands","Transaction_count", "Percentage"))

#Map_insurance
cursor.execute("select * from map_insurance")
mydb.commit()
table3 = cursor.fetchall()

Map_insurance = pd.DataFrame(table3,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count","Transaction_amount"))

#3. Map Transaction

cursor.execute("select * from map_transaction")
mydb.commit()
table3 = cursor.fetchall()

Map_transaction = pd.DataFrame(table3, columns = ("States", "Years","Quarter", "Districts","Transaction_count",
                                                   "Transaction_amount" ))

#4. Map user 

cursor.execute("select * from map_user ")
mydb.commit()
table4= cursor.fetchall()

map_user = pd.DataFrame(table4 , columns = ( "States", "Years","Quarter","Districts", "RegisteredUser", "AppOpens" ))

#Top_insurance
cursor.execute("select * from top_insurance")
mydb.commit()
table5 = cursor.fetchall()

Top_insurance = pd.DataFrame(table5,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))

#top_transaction

cursor.execute("select * from top_transaction")
mydb.commit()
table5 = cursor.fetchall()

top_transaction = pd.DataFrame( table5, columns = ("States", "Years","Quarter","Entity_Name","Transaction_count","Transaction_amount"))

# 6. Top User

cursor.execute("select * from top_user ")
mydb.commit()
table6 = cursor.fetchall()

Top_user = pd.DataFrame(table6, columns = ("States", "Years","Quarter","Districts", "RegisteredUser"))


def Aggre_insurance_Y(df,year):
    aiy= df[df["Years"] == year]
    aiy.reset_index(drop= True, inplace= True)

    aiyg=aiy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    aiyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(aiyg, x="States", y= "Transaction_amount",title= f"{year} TRANSACTION AMOUNT",
                           width=600, height= 650, color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount)
    with col2:

        fig_count= px.bar(aiyg, x="States", y= "Transaction_count",title= f"{year} TRANSACTION COUNT",
                          width=600, height= 650, color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_count)

    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name_tra.sort()
        

        fig_india_1= px.choropleth(aiyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_amount", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyg["Transaction_amount"].min(),aiyg["Transaction_amount"].max()),
                                 hover_name= "States",title = f"{year} TRANSACTION AMOUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_1.update_geos(visible =False)
        
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2= px.choropleth(aiyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_count", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyg["Transaction_count"].min(),aiyg["Transaction_count"].max()),
                                 hover_name= "States",title = f"{year} TRANSACTION COUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_2.update_geos(visible =False)
        
        st.plotly_chart(fig_india_2)

    return aiy


def Aggre_insurance_Y_Q(df,quarter):
    aiyq= df[df["Quarter"] == quarter]
    aiyq.reset_index(drop= True, inplace= True)

    aiyqg= aiyq.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    aiyqg.reset_index(inplace= True)

    col1,col2= st.columns(2)

    with col1:
        fig_q_amount= px.bar(aiyqg, x= "States", y= "Transaction_amount", 
                            title= f"{aiyq['Years'].min()} AND {quarter} TRANSACTION AMOUNT",width= 600, height=650,
                            color_discrete_sequence=px.colors.sequential.Burg_r)
        st.plotly_chart(fig_q_amount)

    with col2:
        fig_q_count= px.bar(aiyqg, x= "States", y= "Transaction_count", 
                            title= f"{aiyq['Years'].min()} AND {quarter} TRANSACTION COUNT",width= 600, height=650,
                            color_discrete_sequence=px.colors.sequential.Cividis_r)
        st.plotly_chart(fig_q_count)

    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name_tra.sort()

        fig_india_1= px.choropleth(aiyqg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_amount", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyqg["Transaction_amount"].min(),aiyqg["Transaction_amount"].max()),
                                 hover_name= "States",title = f"{aiyq['Years'].min()} AND {quarter} TRANSACTION AMOUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_1.update_geos(visible =False)
        
        st.plotly_chart(fig_india_1)
    with col2:

        fig_india_2= px.choropleth(aiyqg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_count", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyqg["Transaction_count"].min(),aiyqg["Transaction_count"].max()),
                                 hover_name= "States",title = f"{aiyq['Years'].min()} AND {quarter} TRANSACTION COUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_2.update_geos(visible =False)
        
        st.plotly_chart(fig_india_2)
    
    return aiyq


def Aggre_Transaction_type(df, state):
    df_state= df[df["States"] == state]
    df_state.reset_index(drop= True, inplace= True)

    agttg= df_state.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    agttg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_hbar_1= px.bar(agttg, x= "Transaction_count", y= "Transaction_type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, width= 600, 
                        title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION COUNT",height= 500)
        st.plotly_chart(fig_hbar_1)

    with col2:

        fig_hbar_2= px.bar(agttg, x= "Transaction_amount", y= "Transaction_type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Greens_r, width= 600,
                        title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION AMOUNT", height= 500)
        st.plotly_chart(fig_hbar_2)
        
        
        
def Aggre_user_plot_1(df,year):
    aguy= df[df["Years"] == year]
    aguy.reset_index(drop= True, inplace= True)
    
    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_line_1= px.bar(aguyg, x="Brands",y= "Transaction_count", title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width=1000,color_discrete_sequence=px.colors.sequential.haline_r)
    st.plotly_chart(fig_line_1)

    return aguy

def Aggre_user_plot_2(df,quarter):
    auqs= df[df["Quarter"] == quarter]
    auqs.reset_index(drop= True, inplace= True)

    fig_pie_1= px.pie(data_frame=auqs, names= "Brands", values="Transaction_count", hover_data= "Percentage",
                      width=1000,title=f"{quarter} QUARTER TRANSACTION COUNT PERCENTAGE",hole=0.5, color_discrete_sequence= px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_pie_1)

    return auqs

def Aggre_user_plot_3(df,state):
    aguqy= df[df["States"] == state]
    aguqy.reset_index(drop= True, inplace= True)

    aguqyg= pd.DataFrame(aguqy.groupby("Brands")["Transaction_count"].sum())
    aguqyg.reset_index(inplace= True)

    fig_scatter_1= px.line(aguqyg, x= "Brands", y= "Transaction_count", markers= True,width=1000)
    st.plotly_chart(fig_scatter_1)

def map_insure_plot_1(df,state):
    miys= df[df["States"] == state]
    miysg= miys.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    miysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_bar_1= px.bar(miysg, x= "Districts", y= "Transaction_amount",
                              width=600, height=500, title= f"{state.upper()} DISTRICTS TRANSACTION AMOUNT",
                              color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_bar_1)

    with col2:
        fig_map_bar_1= px.bar(miysg, x= "Districts", y= "Transaction_count",
                              width=600, height= 500, title= f"{state.upper()} DISTRICTS TRANSACTION COUNT",
                              color_discrete_sequence= px.colors.sequential.Mint)
        
        st.plotly_chart(fig_map_bar_1)

def map_insure_plot_2(df,state):
    miys= df[df["States"] == state]
    miysg= miys.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    miysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_pie_1= px.pie(miysg, names= "Districts", values= "Transaction_amount",
                              width=600, height=500, title= f"{state.upper()} DISTRICTS TRANSACTION AMOUNT",
                              hole=0.5,color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_pie_1)

    with col2:
        fig_map_pie_1= px.pie(miysg, names= "Districts", values= "Transaction_count",
                              width=600, height= 500, title= f"{state.upper()} DISTRICTS TRANSACTION COUNT",
                              hole=0.5,  color_discrete_sequence= px.colors.sequential.Oranges_r)
        
        st.plotly_chart(fig_map_pie_1)

def map_user_plot_1(df, year):
    muy= df[df["Years"] == year]
    muy.reset_index(drop= True, inplace= True)
    muyg= muy.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyg.reset_index(inplace= True)

    fig_map_user_plot_1= px.line(muyg, x= "States", y= ["RegisteredUser","AppOpens"], markers= True,
                                width=1000,height=800,title= f"{year} REGISTERED USER AND APPOPENS", color_discrete_sequence= px.colors.sequential.Viridis_r)
    st.plotly_chart(fig_map_user_plot_1)

    return muy

def map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"] == quarter]
    muyq.reset_index(drop= True, inplace= True)
    muyqg= muyq.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_map_user_plot_1= px.line(muyqg, x= "States", y= ["RegisteredUser","AppOpens"], markers= True,
                                title= f"{df['Years'].min()}, {quarter} QUARTER REGISTERED USER AND APPOPENS",
                                width= 1000,height=800,color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_map_user_plot_1)

    return muyq

def map_user_plot_3(df, state):
    muyqs= df[df["States"] == state]
    muyqs.reset_index(drop= True, inplace= True)
    muyqsg= muyqs.groupby("Districts")[["RegisteredUser", "AppOpens"]].sum()
    muyqsg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_user_plot_1= px.bar(muyqsg, x= "RegisteredUser",y= "Districts",orientation="h",
                                    title= f"{state.upper()} REGISTERED USER",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_plot_1)

    with col2:
        fig_map_user_plot_2= px.bar(muyqsg, x= "AppOpens", y= "Districts",orientation="h",
                                    title= f"{state.upper()} APPOPENS",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_plot_2)

def top_user_plot_1(df,year):
    tuy= df[df["Years"] == year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["States","Quarter"])["RegisteredUser"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuyg, x= "States", y= "RegisteredUser", barmode= "group", color= "Quarter",
                            width=1000, height= 800, color_continuous_scale= px.colors.sequential.Burgyl)
    st.plotly_chart(fig_top_plot_1)

    return tuy

def top_user_plot_2(df,state):
    tuys= df[df["States"] == state]
    tuys.reset_index(drop= True, inplace= True)

    tuysg= pd.DataFrame(tuys.groupby("Quarter")["RegisteredUser"].sum())
    tuysg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuys, x= "Quarter", y= "RegisteredUser",barmode= "group",
                           width=1000, height= 800,color= "RegisteredUser",hover_data="Pincodes",
                            color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_1)

#Streamlit part

st.set_page_config(layout= "wide")

st.title(" 📱 PHONEPE DATA VISUALIZATION AND EXPLORATION by mukul sharma")
st.write("")

with st.sidebar:
    select= option_menu("Main Menu",["Home", "Data Exploration", "Top Charts"])


if select == "Home":

    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.video("https://www.youtube.com/watch?v=oPsN7b4s7LA")

    col3,col4= st.columns(2)
    
    
if select == "Data Exploration":
    tab1, tab2, tab3= st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:
        method = st.radio("**Select the Analysis Method**",["Insurance Analysis", "Transaction Analysis", "User Analysis"])

        if method == "Insurance Analysis":
            col1,col2= st.columns(2)
            with col1:
                years= st.slider("**Select the Year**", Aggre_insurance["Years"].min(), Aggre_insurance["Years"].max(),Aggre_insurance["Years"].min())

            df_agg_insur_Y= Aggre_insurance_Y(Aggre_insurance,years)
            
            col1,col2= st.columns(2)
            with col1:
                quarters= st.slider("**Select the Quarter**", df_agg_insur_Y["Quarter"].min(), df_agg_insur_Y["Quarter"].max(),df_agg_insur_Y["Quarter"].min())

            Aggre_insurance_Y_Q(df_agg_insur_Y, quarters)

            
        elif method == "Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_at= st.slider("**Select the Year**", Aggre_transaction["Years"].min(), Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())

            df_agg_tran_Y= Aggre_insurance_Y(Aggre_transaction,years_at)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_at= st.slider("**Select the Quarter**", df_agg_tran_Y["Quarter"].min(), df_agg_tran_Y["Quarter"].max(),df_agg_tran_Y["Quarter"].min())

            df_agg_tran_Y_Q= Aggre_insurance_Y_Q(df_agg_tran_Y, quarters_at)
            
        elif method == "Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_at= st.slider("**Select the Year**", Aggre_transaction["Years"].min(), Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())

            df_agg_tran_Y= Aggre_insurance_Y(Aggre_transaction,years_at)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_at= st.slider("**Select the Quarter**", df_agg_tran_Y["Quarter"].min(), df_agg_tran_Y["Quarter"].max(),df_agg_tran_Y["Quarter"].min())

            df_agg_tran_Y_Q= Aggre_insurance_Y_Q(df_agg_tran_Y, quarters_at)
            



#question part

def ques1():
    brand= Aggre_user[["Brands","Transaction_count"]]
    brand1=brand.groupby("Brands")["Transaction_count"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index()

    fig_brands= px.pie(brand2, values= "Transaction_count", names = "Brands", 
                        color_discrete_sequence= px.colors.sequential.dense_r, title="Top Mobile Brands of Transaction_count")
    
    return st.plotly_chart(fig_brands)

def ques2():
    ltm = Aggre_transaction[["States","Transaction_amount"]]
    lt1= ltm.groupby("States")["Transaction_amount"].sum().sort_values(ascending= True)
    lt2= pd.DataFrame(lt1).reset_index().head(10)

    fig_lts = px.bar(lt2, x = "States", y = "Transaction_amount", title = " STATES WITH LOWEST TRANSACTION AMOUNT",
                      color_discrete_sequence= px.colors.sequential.Oranges_r)
    
    return st.plotly_chart(fig_lts)

def ques3():
    
    dhtm= Map_transaction[["Districts", "Transaction_amount"]]
    htm1= dhtm.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending= False)
    htm2= pd.DataFrame(htm1).head(10).reset_index()

    fig_htm= px.pie(htm2, values="Transaction_amount", names = "Districts", title= "TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT",
                     color_discrete_sequence=px.colors.sequential.Emrld_r)
    
    return st.plotly_chart(fig_htm)


def ques4():
     
    dltm =Map_transaction[["Districts", "Transaction_amount"]]
    dlm1= dltm.groupby("Districts") ["Transaction_amount"].sum().sort_values(ascending= False)
    dlm2= pd.DataFrame(dlm1).head(10).reset_index()

    fig_dlm= px.pie(dlm2, values= "Transaction_amount" , names = "Districts", title = "Top 10 Districts With Lowest Transaction Amount",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
    
    return st.plotly_chart(fig_dlm)
    
def ques5():
    
    st_appopens= map_user[["States", "AppOpens"]]
    sa1=st_appopens.groupby("States") ["AppOpens"].sum().sort_values(ascending= False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x ="States", y = "AppOpens", title = "Top 10 States With AppOpens",
                    color_discrete_sequence= px.colors.sequential.deep_r)
    
    return st.plotly_chart(fig_sa)

def ques6():
     
    lo_appopens= map_user[["States", "AppOpens"]]
    lap1= lo_appopens.groupby("States") ["AppOpens"].sum().sort_values(ascending=True)
    lap2= pd.DataFrame(lap1).reset_index().head(10)
    
    fig_lap= px.bar(lap2, x="States" , y ="AppOpens", title = "Lowest 10 States With AppOpens",
                     color_discrete_sequence=px.colors.sequential.dense_r)
    
    return st.plotly_chart(fig_lap)

def ques7():
    
    sltc=Aggre_transaction[["States", "Transaction_count"]]
    ltc1= sltc.groupby("States")["Transaction_count"].sum().sort_values(ascending=True)
    ltc2= pd .DataFrame(ltc1).reset_index()

    fig_ltc= px.bar(ltc2, x = "States", y = "Transaction_count", title= "STATES WITH LOWEST TRANSACTION COUNT",
                     color_discrete_sequence=px.colors.sequential.Jet_r)
    return st.plotly_chart(fig_ltc) 

def ques8():
    
    shtc=Aggre_transaction[["States", "Transaction_count"]]
    htc1= shtc.groupby("States")["Transaction_count"].sum().sort_values(ascending=False)
    htc2= pd.DataFrame(htc1).reset_index()

    fig_htc= px.bar(htc2, x = "States", y = "Transaction_count", title= "STATES WITH  HIGHEST  TRANSACTION COUNT",
                     color_discrete_sequence=px.colors.sequential.Magenta_r)
    
    return st.plotly_chart(fig_htc) 

def ques9():
     
     shta=Aggre_transaction[["States", "Transaction_amount"]]
     shta1=shta.groupby("States")["Transaction_amount"].sum().sort_values(ascending= False)
     shta2=pd.DataFrame(shta1).reset_index()

     fig_ta=px.bar(shta2, x = "States", y = "Transaction_amount", title= "HIGHEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
     
     return st.plotly_chart(fig_ta)
    
def ques10():

     dlta= Map_transaction[["Districts", "Transaction_amount"]]    
     dlt1=dlta.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
     dlt2= pd.DataFrame(dlt1).reset_index().head(50)


     fig_lta=px.bar(dlt2, x = "Districts", y = "Transaction_amount", title ="DISTRICTS WITH LOWEST TRANSACTION AMOUNT",
                     color_discrete_sequence= px.colors.sequential.Mint_r)
     
     return st.plotly_chart(fig_lta)
     


select= option_menu("Main Menu",["Please select the question below"]) 


if select == "Please select the question below":

    ques= st.selectbox("**Select the Question**",('Click Here','Top Brands Of Mobiles Used','States With Lowest Trasaction Amount',
                                  'Districts With Highest Transaction Amount','Top 10 Districts With Lowest Transaction Amount',
                                  'Top 10 States With AppOpens','Least 10 States With AppOpens','States With Lowest Trasaction Count',
                                 'States With Highest Trasaction Count','States With Highest Trasaction Amount',
                                 'Top 50 Districts With Lowest Transaction Amount'))
    

if ques=="Top Brands Of Mobiles Used":
        ques1()

elif ques=="States With Lowest Trasaction Amount":
           ques2()

elif ques=='Districts With Highest Transaction Amount':
            ques3()
     
elif ques=='Top 10 Districts With Lowest Transaction Amount':
            ques4()

elif ques=='Top 10 States With AppOpens':
            ques5()

elif ques=='Least 10 States With AppOpens':
            ques6()

elif ques=='States With Lowest Trasaction Count':
            ques7()

elif ques=='States With Highest Trasaction Count':
            ques8()

elif ques=='States With Highest Trasaction Amount':
            ques9()   

elif ques=='Top 50 Districts With Lowest Transaction Amount':
            ques10() 
            
            
            
## DONE HAPPILY WITH LONG EFFORTS