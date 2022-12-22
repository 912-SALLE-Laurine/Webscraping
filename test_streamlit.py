import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import datetime

# doc : https://docs.streamlit.io/library/api-reference
# colorpalet https://coolors.co/palette/ccd5ae-e9edc9-fefae0-faedcd-d4a373
# Functions

def plot_consumption_linecharts(df, title, xaxis_title, yaxis_title, xcolumn, ycolumn):
    # multiple subplots for each category of profile
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=("RES", "PRO", "ENT"))

    fig.add_trace(go.Line(x=df[df["Catégorie profil"] == "RES"][xcolumn], y=df[df["Catégorie profil"] == "RES"][ycolumn]),
                row=1, col=1)

    fig.add_trace(go.Line(x=df[df["Catégorie profil"] == "PRO"][xcolumn], y=df[df["Catégorie profil"] == "PRO"][ycolumn]),
                row=1, col=2)

    fig.add_trace(go.Line(x=df[df["Catégorie profil"] == "ENT"][xcolumn], y=df[df["Catégorie profil"] == "ENT"][ycolumn]),
                row=1, col=3)

    fig.update_layout(height=500, width=1500,
                    title_text=title)

    fig.update_xaxes(title_text=xaxis_title)
    fig.update_yaxes(title_text=yaxis_title)
    # remove legend
    fig.update_layout(showlegend=False)
    #y axis scale from 0 to max value of each subplot
    fig.update_yaxes(range=[0, df[df["Catégorie profil"] == "RES"][ycolumn].max()], row=1, col=1)
    fig.update_yaxes(range=[0, df[df["Catégorie profil"] == "PRO"][ycolumn].max()], row=1, col=2)
    fig.update_yaxes(range=[0, df[df["Catégorie profil"] == "ENT"][ycolumn].max()], row=1, col=3)
    # change color of each subplot
    fig.update_traces(line_color='rgb(96, 108, 56)', row=1, col=1)
    fig.update_traces(line_color='rgb(212, 163, 115)', row=1, col=2)
    fig.update_traces(line_color='rgb(254, 250, 224)', row=1, col=3)
    # background color
    fig.update_layout(plot_bgcolor='rgb(233, 237, 201)')
    return fig

def plot_monthly_consumption_barcharts(df, title, xaxis_title, yaxis_title):
    # multiple subplots for each category of profile
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=("RES", "PRO", "ENT"))

    fig.add_trace(go.Bar(x=df[df["Catégorie profil"] == "RES"]["month"], y=df[df["Catégorie profil"] == "RES"]["Total énergie soutirée (MWh)"]),
                row=1, col=1)

    fig.add_trace(go.Bar(x=df[df["Catégorie profil"] == "PRO"]["month"], y=df[df["Catégorie profil"] == "PRO"]["Total énergie soutirée (MWh)"]),
                row=1, col=2)

    fig.add_trace(go.Bar(x=df[df["Catégorie profil"] == "ENT"]["month"], y=df[df["Catégorie profil"] == "ENT"]["Total énergie soutirée (MWh)"]),
                row=1, col=3)

    fig.update_layout(height=500, width=1500,
                    title_text=title)

    fig.update_xaxes(title_text=xaxis_title)
    fig.update_yaxes(title_text=yaxis_title)
    # remove legend
    fig.update_layout(showlegend=False)
    #y axis scale from 0 to max value of each subplot
    fig.update_yaxes(range=[0, df[df["Catégorie profil"] == "RES"]["Total énergie soutirée (MWh)"].max()], row=1, col=1)
    fig.update_yaxes(range=[0, df[df["Catégorie profil"] == "PRO"]["Total énergie soutirée (MWh)"].max()], row=1, col=2)
    fig.update_yaxes(range=[0, df[df["Catégorie profil"] == "ENT"]["Total énergie soutirée (MWh)"].max()], row=1, col=3)
    # change color of each subplot 
    fig.update_traces(marker_color='rgb(96, 108, 56)', row=1, col=1)
    fig.update_traces(marker_color='rgb(212, 163, 115)', row=1, col=2)
    fig.update_traces(marker_color='rgb(254, 250, 224)', row=1, col=3)
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

# Set page config
st.set_page_config(page_title="Consommation d'énergie et météo", page_icon=":sunny:", layout="wide")
st.title("Consommation d'énergie et météo")


# Set sidebar 
st.sidebar.header("Menu")

# create sidebar menu 
option = st.sidebar.selectbox("Choose an option", ( "Consommation d'énergie totale sur 3 ans", "Consommation d'énergie totale par an", "Consommation d'énergie par an par secteur", "Consommation d'énergie par mois par secteur", "Consommation d'énergie par jour par secteur"))


# Charge datasets
df_3years_agg_sec = pd.read_csv("conso-inf36-region-agg.csv")
df_3years_agg_sec["month"] = df_3years_agg_sec["date"].str[5:7]
df_3years_agg = df_3years_agg_sec.groupby("date").sum().reset_index()

df_agg_month = pd.read_csv("conso-inf36-region-agg-month.csv")

df_total = pd.read_csv("conso-inf36-region-clean.csv", sep=",")

#agg_idf2020 = pd.read_csv("agg_datasets/idf2020_agg.csv")
#agg_idf2020_month = pd.read_csv("agg_datasets/idf2020_month_agg.csv")
#idf2020 = pd.read_csv("datasets/idf2020_clean.csv", sep=";")



# Plot 1 : Consommation d'énergie France sur 3 ans 
if option == "Consommation d'énergie totale sur 3 ans":
    # subtitle
    st.markdown("### Consommation d'énergie en France entre 2020 et 2022")
    st.markdown("---")
    #st.write(df_3years_agg)
    fig = plot_chart(df_3years_agg, "Consommation d'énergie France entre 2020 et 2022", "date", "Energie soutirée (MWh)", "date", "Total énergie soutirée (MWh)")
    st.plotly_chart(fig)

# Plot 2 : Consommation d'énergie en Ile-de-France par mois en 2020
if option == "Consommation d'énergie totale par an":
    st.markdown("### Consommation d'énergie en France pour chaque année")
    st.markdown("---")
    # selector for year
    year = st.selectbox("Choose a year", ("2022", "2021", "2020"))
    # create condition of year 
    if year == "2020":
        df_year = df_3years_agg[df_3years_agg["date"].str.contains("2020")]
        fig = plot_chart(df_year, "Consommation d'énergie France en 2020", "date", "Energie soutirée (MWh)", "date", "Total énergie soutirée (MWh)")
        st.plotly_chart(fig)
    elif year == "2021":
        df_year = df_3years_agg[df_3years_agg["date"].str.contains("2021")]
        fig = plot_chart(df_year, "Consommation d'énergie France en 2021", "date", "Energie soutirée (MWh)", "date", "Total énergie soutirée (MWh)")
        st.plotly_chart(fig)
    elif year == "2022":
        df_year = df_3years_agg[df_3years_agg["date"].str.contains("2022")]
        fig = plot_chart(df_year, "Consommation d'énergie France en 2022", "date", "Energie soutirée (MWh)", "date", "Total énergie soutirée (MWh)")
        st.plotly_chart(fig)


# Plot 3 : Consommation d'énergie par an par secteur
if option == "Consommation d'énergie par an par secteur":
    st.markdown("### Consommation d'énergie en France pour chaque année et chaque secteur")
    st.markdown("---")
    # selector for year
    year = st.selectbox("Choose a year", ("2022", "2021", "2020"))
    # create condition of year 
    if year == "2020":
        df_year = df_agg_month[df_agg_month["year"] == 2020]
        fig = plot_monthly_consumption_barcharts(df_year, "Consommation d'énergie par secteur", "Mois", "Energie soutirée (MWh)")
        st.plotly_chart(fig)
    elif year == "2021":
        df_year = df_agg_month[df_agg_month["year"] == 2021]
        fig = plot_monthly_consumption_barcharts(df_year, "Consommation d'énergie par secteur", "Mois", "Energie soutirée (MWh)")
        st.plotly_chart(fig)
    elif year == "2022":
        df_year = df_agg_month[df_agg_month["year"] == 2022]
        fig = plot_monthly_consumption_barcharts(df_year, "Consommation d'énergie par secteur", "Mois", "Energie soutirée (MWh)")
        st.plotly_chart(fig)


# Plot 4 : Consommation d'énergie sur un mois par secteur 
if option == "Consommation d'énergie par mois par secteur":
    st.markdown("### Consommation d'énergie en France pour chaque mois et chaque secteur")
    st.markdown("---")
    # choose a year 
    year = st.selectbox("Choose a year", ("2022", "2021", "2020"))
    # choose a month 
    month = st.selectbox("Choose a month", ("Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"))
    # dictionnary to convert month in number
    month_dict = {"Janvier": "01", "Février": "02", "Mars": "03", "Avril": "04", "Mai": "05", "Juin": "06", "Juillet": "07", "Août": "08", "Septembre": "09", "Octobre": "10", "Novembre": "11", "Décembre": "12"}
    # convert month in number
    month = month_dict[month]
    year_month = year + "-" + month
    # create condition of year
    df_year_month = df_3years_agg_sec[df_3years_agg_sec["date"].str.contains(year_month)]
    fig = plot_consumption_linecharts(df_year_month, "Energie soutirée par profil", "date", "Energie soutirée (MWh)", "date", "Total énergie soutirée (MWh)")
    st.plotly_chart(fig)


# Plot 5 : Consommation d'énergie sur un jour par secteur
if option == "Consommation d'énergie par jour par secteur":
    st.markdown("### Consommation d'énergie en France pour chaque jour et chaque secteur")
    st.markdown("---")
    # choose a year 
    year = st.selectbox("Choose a year", ("2022", "2021", "2020"))
    # choose a month 
    month = st.selectbox("Choose a month", ("Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"))
    # dictionnary to convert month in number
    month_dict = {"Janvier": "01", "Février": "02", "Mars": "03", "Avril": "04", "Mai": "05", "Juin": "06", "Juillet": "07", "Août": "08", "Septembre": "09", "Octobre": "10", "Novembre": "11", "Décembre": "12"}
    # convert month in number
    month = month_dict[month]
    # choose a day
    day = st.selectbox("Choose a day", ("01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"))
    year_month_day = year + "-" + month + "-" + day
    #st.write(df_total.iloc[:20,])
    # create condition of year
    df_year_month_day = df_total[df_total["date"].str.contains(year_month_day)]
    #st.write(df_year_month_day)
    df_year_month_day_agg = df_year_month_day.groupby(["Catégorie profil", "time"]).agg({"Total énergie soutirée (MWh)": "sum"}).reset_index()
    #st.write(df_year_month_day_agg)
    fig = plot_consumption_linecharts(df_year_month_day_agg, "Energie soutirée par profil", "time", "Energie soutirée (MWh)", "time", "Total énergie soutirée (MWh)")
    st.plotly_chart(fig)
