import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import datetime
import requests

# doc : https://docs.streamlit.io/library/api-reference
# colorpalet https://coolors.co/palette/ccd5ae-e9edc9-fefae0-faedcd-d4a373
# Functions

def plot_consumption_linecharts(df, title, xaxis_title, yaxis_title, xcolumn, ycolumn):
    # multiple subplots for each category of profile
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("RES", "PRO"))

    fig.add_trace(go.Line(x=df[df["Catégorie profil"] == "RES"][xcolumn], y=df[df["Catégorie profil"] == "RES"][ycolumn]),
                row=1, col=1)

    fig.add_trace(go.Line(x=df[df["Catégorie profil"] == "PRO"][xcolumn], y=df[df["Catégorie profil"] == "PRO"][ycolumn]),
                row=1, col=2)

    fig.update_layout(height=500, width=900,
                    title_text=title)

    fig.update_xaxes(title_text=xaxis_title)
    fig.update_yaxes(title_text=yaxis_title)
    # remove legend
    fig.update_layout(showlegend=False)
    #y axis scale from 0 to max value of each subplot
    fig.update_yaxes(range=[0, df[df["Catégorie profil"] == "RES"][ycolumn].max()], row=1, col=1)
    fig.update_yaxes(range=[0, df[df["Catégorie profil"] == "PRO"][ycolumn].max()], row=1, col=2)
    # change color of each subplot
    fig.update_traces(line_color='rgb(96, 108, 56)', row=1, col=1)
    fig.update_traces(line_color='rgb(212, 163, 115)', row=1, col=2)
    # background color
    fig.update_layout(plot_bgcolor='rgb(233, 237, 201)')
    return fig

def plot_monthly_consumption_barcharts(df, title, xaxis_title, yaxis_title):
    # multiple subplots for each category of profile
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("RES", "PRO"))

    fig.add_trace(go.Bar(x=df[df["Catégorie profil"] == "RES"]["Month"], y=df[df["Catégorie profil"] == "RES"]["Total énergie soutirée (MWh)"]),
                row=1, col=1)

    fig.add_trace(go.Bar(x=df[df["Catégorie profil"] == "PRO"]["Month"], y=df[df["Catégorie profil"] == "PRO"]["Total énergie soutirée (MWh)"]),
                row=1, col=2)

    fig.update_layout(height=500, width=900,
                    title_text=title)

    fig.update_xaxes(title_text=xaxis_title)
    fig.update_yaxes(title_text=yaxis_title)
    # remove legend
    fig.update_layout(showlegend=False)
    #y axis scale from 0 to max value of each subplot
    fig.update_yaxes(range=[0, df[df["Catégorie profil"] == "RES"]["Total énergie soutirée (MWh)"].max()], row=1, col=1)
    fig.update_yaxes(range=[0, df[df["Catégorie profil"] == "PRO"]["Total énergie soutirée (MWh)"].max()], row=1, col=2)
    # change color of each subplot 
    fig.update_traces(marker_color='rgb(96, 108, 56)', row=1, col=1)
    fig.update_traces(marker_color='rgb(212, 163, 115)', row=1, col=2)
    # background color
    fig.update_layout(plot_bgcolor='rgb(233, 237, 201)')
    return fig

# plot a unique chart function 
def plot_chart(df, title, xaxis_title, yaxis_title, xcolumn, ycolumn, ycolumn2 = None, yaxis_title2 = None, trace_name = None, trace_name2 = None):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Line(x=df[xcolumn], y=df[ycolumn], yaxis = "y1", line = {'color': 'rgb(96, 108, 56)'}), secondary_y=False)

    if ycolumn2 != None:
        # add a second y axis 
        fig.add_trace(go.Line(x=df[xcolumn], y=df[ycolumn2], yaxis = "y2", line={'color': 'rgb(212, 163, 115)'}), secondary_y=True)    
        fig.update_layout(yaxis2=dict(overlaying="y", side="right"))
    # set traces name
    fig.update_traces(name=trace_name)
    fig.update_traces(name=trace_name2, secondary_y=True)

    # adapt height and width of the chart to the size of the screen
    fig.update_layout(height=500, width=900,
                    title_text=title)
    fig.update_xaxes(title_text=xaxis_title)
    fig.update_yaxes(title_text=yaxis_title, secondary_y=False)
    fig.update_yaxes(title_text=yaxis_title2, secondary_y=True)
    #y axis scale from 0 to max value of each subplot
    if min(df[ycolumn] > 0) : 
        fig.update_yaxes(range=[0, df[ycolumn].max()], secondary_y=False)
    else : 
        fig.update_yaxes(range=[df[ycolumn].min(), df[ycolumn].max()], secondary_y=False)
    # same for y2 column 
    if ycolumn2 != None:
        fig.update_yaxes(range=[0, df[ycolumn2].max()], secondary_y=True)
    # change background color
    fig.update_layout(plot_bgcolor='rgb(233, 237, 201)')
    return fig

def plot_map(df, title):
    # import geojson region file with url 
    geojson = requests.get('https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions.geojson').json()
    # create a france map and color each region with the total energy consumption
    fig = px.choropleth_mapbox(df, geojson=geojson, locations='Région', color='Total énergie soutirée (MWh)',
                            color_continuous_scale="YlGn",
                            mapbox_style="carto-positron",
                            zoom=3.5, center = {"lat": 46.2276, "lon": 2.2137},
                            opacity=0.8,
                            labels={'Total énergie soutirée (MWh)':'Total énergie soutirée (MWh)'}, 
                            featureidkey= "properties.nom", 
                            title = title)
    # put the title in a visible place
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
    fig.update_layout(height=700, width=900)
    # same but with the values inside the map


    return fig
    
def display_meteo(df):
    
    dict_emoji = {
    'Soleil et partiellement nuageux': '⛅️',
    'Couvert': '☁️',
    'Brouillard': '🌫',
    'Ciel dégagé, pleinement ensoleillé': '☀️',
    'Bruine légère': '🌧',
    'Nuageux': '⛅️',
    'Faible pluie en continue': '🌧',
    'Pluie légère et soleil': '🌦☀️',
    'Fortes chutes de neige': '❄️⛄️',
    'Faibles averses de pluie': '🌦',
    'Blizzard': '❄️⛈️',
    'Faibles chûtes de neige': '❄️🌨',
    'Neige abondante en continue': '❄️⛄️',
    'Bruine légère partielle': '🌦',
    'Pluie modérée en continue': '🌧',
    'Faible pluie non continue': '🌦',
    'Pluie modérée non continue': '🌦',
    'Foyers orageux à proximité': '⚡️🌩',
    'Faibles chutes de neige en continue': '❄️',
    'Faibles chutes de neige partiellement': '❄️',
    'Neige fondue en faible quantité': '🌧❄️',
    'Chûtes de neige modérées en continu': '❄️🌨',
    'Faibles averses de neige fondue': '🌧❄️',
    'Forte pluie verglacée': '🌧❄️',
    'Forte pluie et orages': '⛈️🌧',
    'Forte pluie non continue': '🌧',
    'Averses de pluie et orages': '⛈️🌧',
    'Pluie forte ou modéré': '🌧'
}
    # display the weather of the day with an icon
    st.subheader("Météo du jour ")
    # display df
    
    # df2 = df[["day", "tempMax", "tempMin", "windSpeed", "precipitation"]]
    # # rename all columns
    # df2.columns = ["Date", "Température maximale", "Température minimale", "Vitesse du vent moyenne", "Précipitation"]
    # # remove the index column
    # df2 = df2.set_index("Date")
    # st.write(df2)
    # st.write("Météo à 13h :")
    # st.metric( df["meteo_13h"].iloc[0] ,dict_emoji[df["meteo_13h"].iloc[0]])

    # create 4 columns
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric(  df["meteo_13h"].iloc[0] ,dict_emoji[df["meteo_13h"].iloc[0]])
    with col2:
        st.metric( "Température à 13h", df["temp_13h"].iloc[0] + "C")
    with col3:
        st.metric( "Température maximale", df["tempMax"].iloc[0] + "C")
    with col4:
        st.metric( "Température minimale", df["tempMin"].iloc[0] + "C")
    with col5:
        st.metric( "Vitesse du vent moyenne", df["windSpeed"].iloc[0])

# calcul coefficient de corrélation fonction
def corr_coef(df, col1, col2):
    # get the correlation coefficient
    corr = df[col1].corr(df[col2])
    #arrondir r 
    corr = round(corr, 2)
    # get the p value
    #p_value = stats.pearsonr(df[col1], df[col2])[1]
    st.metric("Coefficient de corrélation", corr)

    # return the correlation coefficient and the p value
    return corr

# Set page config
st.set_page_config(page_title="Data visualisations", page_icon =":sunny:",  layout="wide")
st.title("Consommation d'énergie et météo")


# Set sidebar 
st.sidebar.header("Menu")

# create sidebar menu 
option = st.sidebar.selectbox("Choisir une visualisation", ("Consommation d'énergie totale sur 3 ans", "Consommation d'énergie par an par secteur", "Consommation d'énergie par mois par secteur", "Consommation d'énergie par jour par secteur", "Cartographie de la consommation sur une journée"))
# add another sidebar menu to choose the region 
region = st.sidebar.selectbox("Choisir une région", ("France entière", "Île-de-France", "Auvergne-Rhône-Alpes"))

month_dict = {"Janvier": "01", "Février": "02", "Mars": "03", "Avril": "04", "Mai": "05", "Juin": "06", "Juillet": "07", "Août": "08", "Septembre": "09", "Octobre": "10", "Novembre": "11", "Décembre": "12"}


# Plot 1 : Consommation d'énergie France sur 3 ans 
if option == "Consommation d'énergie totale sur 3 ans":

    # initialize dataframe empty
    df = pd.DataFrame()
    if region == "France entière":
        st.markdown("### Consommation d'énergie en France entre 2020 et 2022")
        st.markdown("---")
        df = pd.read_csv("conso-inf36-region-agg.csv")
        #df["month"] = df["date"].str[5:7]
        df = df.groupby("Date").sum().reset_index()
        fig = plot_chart(df, "Consommation d'énergie entre 2020 et 2022", "Date", "Energie soutirée (MWh)", "Date", "Total énergie soutirée (MWh)")
        st.plotly_chart(fig)
        st.info("Nous constatons des cycles : forte consommation en hiver, et faible en été, avec un facteur 2 de différence.")

    else :
        st.markdown("### Consommation d'énergie en " + region + " entre 2020 et 2022")
        st.markdown("---")
        df = pd.read_csv("regions_datasets_agg/conso-inf36-" + region + "-agg.csv")
        df = df.groupby("Date").sum().reset_index()
        # checkbox add meteo
        if st.checkbox("Tracer la Température"):
            df_meteo = pd.read_csv("meteo_datasets/meteo-" + region + ".csv")
            # change the date format to match the other dataframe in a new column
            df_meteo["Date"] = df_meteo["day"].str[0:4] + "-" + df_meteo["day"].str[5:7] + "-" +df_meteo["day"].str[8:10] 
            # transform the temperatureremove the °C
            df_meteo["temp_13h"] = df_meteo["temp_13h"].str.replace("°", "")
            # convert the column to float
            df_meteo["temp_13h"] = df_meteo["temp_13h"].astype(float)
            # merge the 2 dataframes with day and Date as key 
            df = pd.merge(df, df_meteo, how="left", left_on="Date", right_on="Date")
            #st.write(df)
            fig = plot_chart(df, "Consommation d'énergie et température entre 2020 et 2022", "Date", "Energie soutirée (MWh)", "Date", "Total énergie soutirée (MWh)", "temp_13h", "Température (°C)")
            st.plotly_chart(fig)
            corr_coef(df, "Total énergie soutirée (MWh)", "temp_13h")
            st.info("Nous constatons une forte corrélation négative entre la température et la consommation d'énergie.")

        else : 
            fig = plot_chart(df, "Consommation d'énergie entre 2020 et 2022", "Date", "Energie soutirée (MWh)", "Date", "Total énergie soutirée (MWh)")
            st.plotly_chart(fig)
            st.info("Nous constatons des cycles : forte consommation en hiver, et faible en été, avec un facteur 2 de différence.")

    if st.checkbox("Show dataframe"):
        st.write(df)



# Plot 2 : Consommation d'énergie par an par secteur
elif option == "Consommation d'énergie par an par secteur":

    # initialize dataframe empty
    df = pd.DataFrame()
    if region == "France entière":
        st.markdown("###  Consommation d'énergie en France pour une année et un secteur")
        st.markdown("---")
        df = pd.read_csv("conso-inf36-region-agg-month.csv")
    else :
        st.markdown("### Consommation d'énergie en " + region + " pour une année et un secteur")
        st.markdown("---")
        df = pd.read_csv("regions_datasets_agg/conso-inf36-" + region + "-agg-month.csv")

    year = st.selectbox("Choose a year", ("2020", "2021", "2022"))

    df_year = df[df["Year"] == int(year)]

    fig = plot_monthly_consumption_barcharts(df_year, "Consommation d'énergie par secteur", "Mois", "Energie soutirée (MWh)")
    st.plotly_chart(fig)
    # checkbox to display the dataframe
    st.info("Nous constatons comme dans la 1ère visualisation une différence entre l'hiver et l'été, un peu moins marquée pour le secteur professionnel. En regardant pour 2020, nous voyons que la différence de consommation entre mars et avril est très marquée par rapport aux autres années dans le secteur professionnel, ce qui correspond à une baisse importante de la consommation au début du 1er confinement")
    if st.checkbox("Show dataframe"):
        st.write(df)



# Plot 3 : Consommation d'énergie sur un mois par secteur 
elif option == "Consommation d'énergie par mois par secteur":

    # initialize dataframe empty
    df = pd.DataFrame()
    if region == "France entière":
        st.markdown("###  Consommation d'énergie en France pour un mois et un secteur")
        st.markdown("---")
        df = pd.read_csv("conso-inf36-region-agg.csv")
    else :
        st.markdown("### Consommation d'énergie en " + region + " pour un mois et un secteur")
        st.markdown("---")
        df = pd.read_csv("regions_datasets_agg/conso-inf36-" + region + "-agg.csv")
        meteo = pd.read_csv("meteo_datasets/meteo-" + region + ".csv")

    # choose a year 
    year = st.selectbox("Choose a year", ("2020", "2021", "2022"))

    # choose a month with slider of month with month list
    month_list = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
    # change the color of the slider pointer
    month = st.select_slider("Choose a month", options=month_list)
    Slider_Cursor = st.markdown(''' <style> div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"]{
        background-color: rgb(96, 108, 56); box-shadow: rgb(14 38 74 / 20%) 0px 0px 0px 0.2rem;} </style>''', unsafe_allow_html = True)
    Slider_Number = st.markdown(''' <style> div.stSlider > div[data-baseweb="slider"] > div > div > div > div
                                    { color: rgb(96, 108, 56); } </style>''', unsafe_allow_html = True)
    col = f''' <style> div.stSlider > div[data-baseweb = "slider"] > div > div {{
        background: linear-gradient(to right, rgb(1, 183, 158) 0%, 
                                    rgb(1, 183, 158) {month}%, 
                                    rgba(151, 166, 195, 0.25) {month}%, 
                                    rgba(151, 166, 195, 0.25) 100%); }} </style>'''
    ColorSlider = st.markdown(col, unsafe_allow_html = True)  

    # convert month in number
    month = month_dict[month]
    year_month = year + "-" + month

    #df_3years_agg_sec["month"] = df_3years_agg_sec["date"].str[5:7]
    # create condition of year
    df_year_month = df[df["Date"].str.contains(year_month)]
    fig = plot_consumption_linecharts(df_year_month, "Energie soutirée par profil", "Date", "Energie soutirée (MWh)", "Date", "Total énergie soutirée (MWh)")
    st.plotly_chart(fig)

    if region != "France entière" :
        meteo_date = year + "/" + month
        meteo_year_month = meteo[meteo["day"].str.contains(meteo_date)]
        # transform the temp_13h by removing "°" and transform to int 
        meteo_year_month["temp_13h"] = meteo_year_month["temp_13h"].str.replace("°", "")
        meteo_year_month["temp_13h"] = meteo_year_month["temp_13h"].astype(int)
        # transfom the day column in the form yyyy-mm-dd
        meteo_year_month["day"] = meteo_year_month["day"].str.replace("/", "-")
        # rename day by Date
        meteo_year_month = meteo_year_month.rename(columns={"day": "Date"})
        df = df_year_month[df_year_month["Catégorie profil"] == "RES"]

        # concatenate with df_year_month
        df = pd.merge(df, meteo_year_month, on="Date", how="left")
        # write the dataset 
        
        fig_meteo = plot_chart(df, "Température à 13h de chaque jour", "Date", "Température à 13h (°C)", "Date", "temp_13h")
        # set figure background temperature to light beige
        fig_meteo.update_layout(plot_bgcolor='rgb(238, 227, 190)')
        st.plotly_chart(fig_meteo)

        st.markdown("Remarques :")
        st.markdown("- Les mois de juin 2020, 2021 comportent des pics de chaleur qui se répercutent très peu sur la consommation")
        st.markdown("- Le mois de juin 2022 comporte un pic de chaleur qui dépasse les 35°C. Cela se répercute plus significativement sur la consommation ")
        st.markdown("- Les mois d'hiver tels que novembre 2020, ont des fortes baisses de températur (19°C à 6°C) qui se répercutent clairement en hausse de la consommation")
        
        # et button to show 2 lines in the same chart 
        if st.button("Superposer les courbes de température et consommation"):
            fig_meteo = plot_chart(df, "Température et consommation des résidences", "Date", "Energie soutirée (MWh)", "Date", "Total énergie soutirée (MWh)", "temp_13h", "Température à 13h (°C)", "énergie", "température")
            fig_meteo.update_layout(plot_bgcolor='rgb(238, 227, 190)')
            st.plotly_chart(fig_meteo)
 
        # checkbox to display the dataframe
        if st.checkbox("Show dataframe"):
            st.write(df)
        
        # correlation temperature et consommation fonction 
        coef = corr_coef(df, "temp_13h", "Total énergie soutirée (MWh)")


    st.success("Constat : En été, une grande différence de température au sein d'un mois a en général peu de répercussions sur la consommation électrique du secteur PRO et RES. En hiver, une différence de température significative au sein d'un mois a une répercussion importante sur la consommation, et cela est plus visible sur le secteur RES que PRO")


# Plot 4 : Consommation d'énergie sur un jour par secteur
elif option == "Consommation d'énergie par jour par secteur":
    df = pd.read_csv("conso-inf36-region-only-some-dates.csv", sep=",")
    # empty dataframe
    meteo = pd.DataFrame()
    if region == "France entière":
        st.markdown("###  Consommation d'énergie en France pour un jour pour chaque secteur")
        st.markdown("---")
    else :
        st.markdown("### Consommation d'énergie en " + region + " pour un jour pour chaque secteur")
        st.markdown("---")
        # filter the dataframe by region
        df = df[df["Région"] == region]
        meteo = pd.read_csv("meteo_datasets/meteo-" + region + ".csv")
    # create tabs
    
    col1, col2 = st.tabs(["Vue 1", "Vue 2"])
    with col1:
        year = st.selectbox("Choose a year", ("2020", "2021", "2022"))
        # choose a date among 4 choices : 01-15, 04-15, 07-15, 10-15
        date = st.selectbox("Choose a date", ("15 Janvier", "15 Avril", "15 Juillet", "15 Octobre")) 
        # separate month and day
        month = date.split(" ")[1]
        day = date.split(" ")[0]
        # convert month in number
        month = month_dict[month]
        year_month_day = year + "-" + month + "-" + day

        df_year_month_day = df[df["Date"].str.contains(year_month_day)]
        df_year_month_day_agg = df_year_month_day.groupby(["Catégorie profil", "Horodate"]).agg({"Total énergie soutirée (MWh)": "sum"}).reset_index()
        df_year_month_day_agg["Time"] = df_year_month_day_agg["Horodate"].str[11:16]
        fig = plot_consumption_linecharts(df_year_month_day_agg, "Energie soutirée par profil", "Time", "Energie soutirée (MWh)", "Horodate", "Total énergie soutirée (MWh)")
        # change the size of the plot
        fig.update_layout(height=400, width=900)
        st.plotly_chart(fig)
        st.info("Tendance secteur résidentiel: baisse de consommation la nuit, puis remontée à partir de 6h. Pic de consommation vers 13h, puis baisse et remontée en soirée (à partir de 18h)")
        st.info("Tendance secteur professionnel: baisse de consommation la nuit, puis remontée à partir de 6h. Pic de consommation vers 12h, puis très légère baisse jusqu'à 18h, et baisse drastique en soirée")
        if region != "France entière":
            # extract from meteo dataset the data for the year_month_day
            date = year + "/" + month + "/" + day
            meteo_year_month_day = meteo[meteo["day"].str.contains(date)]
            # st.write(meteo_year_month_day)
            display_meteo(meteo_year_month_day)
    with col2:
        year2 = st.selectbox("Choose a second year", ("2020", "2021", "2022"))
        # choose a date among 4 choices : 01-15, 04-15, 07-15, 10-15
        date2 = st.selectbox("Choose a second date", ("15 Avril", "15 Juillet", "15 Octobre", "15 Janvier"))

        # separate month and day
        month = date2.split(" ")[1]
        day = date2.split(" ")[0]
        # convert month in number
        month = month_dict[month]
        year_month_day = year2 + "-" + month + "-" + day

        df_year_month_day = df[df["Date"].str.contains(year_month_day)]
        #st.write(df_year_month_day)
        df_year_month_day_agg = df_year_month_day.groupby(["Catégorie profil", "Horodate"]).agg({"Total énergie soutirée (MWh)": "sum"}).reset_index()
        # create time column
        df_year_month_day_agg["Time"] = df_year_month_day_agg["Horodate"].str[11:16]
        fig = plot_consumption_linecharts(df_year_month_day_agg, "Energie soutirée par profil", "Time", "Energie soutirée (MWh)", "Horodate", "Total énergie soutirée (MWh)")
        # change the size of the plot
        fig.update_layout(height=400, width=900)
        st.plotly_chart(fig)
        if region != "France entière":
            # extract from meteo dataset the data for the year_month_day
            date = year + "/" + month + "/" + day
            meteo_year_month_day = meteo[meteo["day"].str.contains(date)]
            # st.write(meteo_year_month_day)
            display_meteo(meteo_year_month_day)

# Plot 5 : Cartographie de la consommation sur une journée
elif option == "Cartographie de la consommation sur une journée":
    st.markdown("### Cartographie de la consommation d'énergie en France pour une journée")
    st.markdown("---")
    # choose a year 
    year = st.selectbox("Choose a year", ("2020", "2021", "2022"))
    # choose a date among 4 choices : 01-15, 04-15, 07-15, 10-15 using 
    # choose a date among 4 choices : 01-15, 04-15, 07-15, 10-15
    date = st.radio("Choose a date", ("15 Janvier", "15 Avril", "15 Juillet", "15 Octobre")) 

    # separate month and day
    month = date.split(" ")[1]
    day = date.split(" ")[0]
    # convert month in number
    month = month_dict[month]
    year_month_day = year + "-" + month + "-" + day
    # import the dataset 
    df = pd.read_csv("conso-inf36-region-only-some-dates.csv", sep=",")
    # create condition of year
    df_year_month_day = df[df["Date"].str.contains(year_month_day)]

    df_year_month_day_agg = df_year_month_day.groupby(["Catégorie profil","Région"]).agg({"Total énergie soutirée (MWh)": "sum"}).reset_index()
    fig1 = plot_map(df_year_month_day_agg[df_year_month_day_agg["Catégorie profil"] == "RES"], "Consommation par région pour les résidentiels")
    fig2 = plot_map(df_year_month_day_agg[df_year_month_day_agg["Catégorie profil"] == "PRO"], "Consommation par région pour les professionnels")
    fig1.update_layout(height=300, width=500)
    fig2.update_layout(height=300, width=500)
    
    col1, col2 = st.columns(2)
    with col1:
        
        st.plotly_chart(fig1)
    with col2:
       st.plotly_chart(fig2)

    st.info("Les écarts de consommation entre les régions sont globalement constant, excepté les régions PACA, Occitanie, Nouvelle Aquitaine qui sont plus proches de l'Ile de France et la région Auvergne Rhône Alpes en été qu'en hiver. Cela peut s'expliquer par une consommation de chauffage moins élevée dans ces régions du Sud en hiver (donc différence plus grande avec l'Ile de France), et une consommation de climatisation plus élevée en été (donc augmentation, se rapprochant de l'Ile de France).")
    # checkbox to display the dataframe
    if st.checkbox("Show dataframe"):
        st.write(df_year_month_day_agg)

