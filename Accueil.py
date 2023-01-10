import streamlit as st
st.set_page_config(page_title="Accueil", page_icon =":sunny:",  layout="wide")


st.title("🌩️ Projet : Consommation d'énergie et météo")

st.subheader("Sujet : Y a-t-il un lien entre la consommation d'énergie et la météo ? ")
st.write("Ce projet est réalisé dans le cadre du cours de Webscraping")
col1, col2 = st.tabs(["Hypothèses", "Données"])
with col1 : 
    # liste d'hypothèses 
    st.subheader("Hypothèses :")
    st.markdown("- Le lien entre la consommation d'énergie et la météo s'observe en particulier dans le secteur résidentiel")
    st.markdown("- En hiver, plus la température est basse, plus il y a d'énergie consommée")
    st.markdown("- En été, lors de pics de chaleur, il y a plus d'énergie consommée")

with col2 : 
    st.subheader("Données :")
    st.markdown("#### 1. Données de consommation d'énergie : Données publiques d'Enedis")
    st.info("Lien : https://data.enedis.fr/explore/dataset/conso-inf36-region/information/")
    st.markdown("- Données de 2020 (janvier) à 2022 (septembre)")
    st.markdown("- Pas de 1/2 ")
    st.markdown("- Contient uniquement les souscriptions inférieures à 36 kW/h")
    st.markdown("- Une ligne pour chaque région, chaque interval de souscription, et chaque catégorie (PRO, RES)")
    st.success("Méthode utilisée : Test d'utilisation de l'API fournie mais limitation à 10 000 lignes de données, donc téléchargement de csv ")
    
    st.markdown("#### 2. Données de consommation d'énergie : Données publiques d'Enedis")
    st.info("Lien : https://www.historique-meteo.net/france/")
    st.markdown("- Possibilité de remonter jusqu'en 2009")
    st.markdown("- Météo journalière, par région ")
    st.markdown("- Contient la température, l'humidité, les précipitations, l'état du ciel ")
    st.success("Méthode utilisée : Scraping web des données utiles pour chaque jour ")

st.write("© 2023 - Projet réalisé par Laurine SALLE et Grégoire CAURIER (ESILV A5 - DIA1)")