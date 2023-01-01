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

    fig.update_layout(height=500, width=1500,
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

    fig.update_layout(height=500, width=1500,
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
def plot_chart(df, title, xaxis_title, yaxis_title, xcolumn, ycolumn):
    fig = go.Figure()
    fig.add_trace(go.Line(x=df[xcolumn], y=df[ycolumn]))
    fig.update_layout(height=500, width=1000,
                    title_text=title)
    fig.update_xaxes(title_text=xaxis_title)
    fig.update_yaxes(title_text=yaxis_title)
    # change color of line
    fig.update_traces(line_color='rgb(96, 108, 56)')
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
                            zoom=5, center = {"lat": 46.2276, "lon": 2.2137},
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


    # create a tab
    tab1 , tab2= st.tabs(["Météo", "Prévisions"])
    with tab1 :

        # display the weather of the day with an icon
        st.header("Météo du jour ")
        # display df
        
        df2 = df[["day", "tempMax", "tempMin", "windSpeed", "precipitation"]]
        # rename all columns
        df2.columns = ["Date", "Température maximale", "Température minimale", "Vitesse du vent moyenne", "Précipitation"]
        # remove the index column
        df2 = df2.set_index("Date")
        st.write(df2)
        st.write("Météo à 13h :")
        st.metric( df["meteo_13h"].iloc[0] ,dict_emoji[df["meteo_13h"].iloc[0]])
    with tab2 :
        st.write("test")
    # # display the temperature of the day 
    # st.write("Température à 13h :")
    # st.write(df["temp_13h"].iloc[0])
    # # max temperature
    # st.write("Température maximale :")
    # st.write(df["tempMax"].iloc[0])
    # # min temperature
    # st.write("Température minimale :")
    # st.write(df["tempMin"].iloc[0])
    # # display the wind speed of the day 
    # st.write("Vitesse du vent du jour :")
    # st.write(df["windSpeed"].iloc[0])
    # # display the wind direction of the day 
    # st.write("Pluie :")
    # st.write(df["precipitation"].iloc[0])

# Set page config
st.set_page_config(page_title="Consommation d'énergie et météo", page_icon=":sunny:", layout="wide")
st.title("Consommation d'énergie et météo")

# Set sidebar 
st.sidebar.header("Menu")

# create sidebar menu 
option = st.sidebar.selectbox("Choose an option", ("Consommation d'énergie totale sur 3 ans", "Consommation d'énergie totale par an", "Consommation d'énergie par an par secteur", "Consommation d'énergie par mois par secteur", "Consommation d'énergie par jour par secteur", "Cartographie de la consommation sur une journée"))
# add another sidebar menu to choose the region 
region = st.sidebar.selectbox("Choose a region", ("France entière", "Île-de-France", "Auvergne-Rhône-Alpes"))

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
    else :
        st.markdown("### Consommation d'énergie en " + region + " entre 2020 et 2022")
        st.markdown("---")
        df = pd.read_csv("regions_datasets_agg/conso-inf36-" + region + "-agg.csv")
        df = df.groupby("Date").sum().reset_index()
    
    # plot chart
    fig = plot_chart(df, "Consommation d'énergie entre 2020 et 2022", "Date", "Energie soutirée (MWh)", "Date", "Total énergie soutirée (MWh)")
    st.plotly_chart(fig)

# Plot 2 : Consommation d'énergie en Ile-de-France par mois en 2020
elif option == "Consommation d'énergie totale par an":

    # initialize dataframe empty
    df = pd.DataFrame()
    if region == "France entière":
        st.markdown("###  Consommation d'énergie en France pour une année")
        st.markdown("---")
        df = pd.read_csv("conso-inf36-region-agg.csv")
        df = df.groupby("Date").sum().reset_index()
    else :
        st.markdown("### Consommation d'énergie en " + region + " pour une année")
        st.markdown("---")
        df = pd.read_csv("regions_datasets_agg/conso-inf36-" + region + "-agg.csv")
        df = df.groupby("Date").sum().reset_index()
    
    year = st.selectbox("Choose a year", ("2022", "2021", "2020"))

    df_year = df[df["Date"].str.contains(year)]
    # plot chart
    fig = plot_chart(df_year, "Consommation d'énergie en " + year, "Date", "Energie soutirée (MWh)", "Date", "Total énergie soutirée (MWh)")
    st.plotly_chart(fig)



# Plot 3 : Consommation d'énergie par an par secteur
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

    year = st.selectbox("Choose a year", ("2022", "2021", "2020"))

    df_year = df[df["Year"] == int(year)]

    fig = plot_monthly_consumption_barcharts(df_year, "Consommation d'énergie par secteur", "Mois", "Energie soutirée (MWh)")
    st.plotly_chart(fig)
    # checkbox to display the dataframe
    if st.checkbox("Show dataframe"):
        st.write(df)



# Plot 4 : Consommation d'énergie sur un mois par secteur 
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

    # choose a year 
    year = st.selectbox("Choose a year", ("2022", "2021", "2020"))

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


# Plot 5 : Consommation d'énergie sur un jour par secteur
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
    col1, col2 = st.columns(2)
    with col1:
        year = st.selectbox("Choose a year", ("2022", "2021", "2020"))
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
        fig.update_layout(height=600, width=1000)
        st.plotly_chart(fig)
        if region != "France entière":
            # extract from meteo dataset the data for the year_month_day
            date = year + "/" + month + "/" + day
            meteo_year_month_day = meteo[meteo["day"].str.contains(date)]
            st.write(meteo_year_month_day)
            display_meteo(meteo_year_month_day)
    with col2:
        year2 = st.selectbox("Choose a second year", ("2022", "2021", "2020"))
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
        fig.update_layout(height=600, width=1000)
        st.plotly_chart(fig)

elif option == "Cartographie de la consommation sur une journée":
    st.markdown("### Cartographie de la consommation d'énergie en France pour une journée")
    st.markdown("---")
    # choose a year 
    year = st.selectbox("Choose a year", ("2022", "2021", "2020"))
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
 
    
    col1, col2 = st.columns(2)
    with col1:
        
        st.plotly_chart(fig1)
    with col2:
       st.plotly_chart(fig2)

    # checkbox to display the dataframe
    if st.checkbox("Show dataframe"):
        st.write(df_year_month_day_agg)

