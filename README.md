# Projet webscraping : Consommation d'énergie et météo 
Binôme : Laurine Sallé et Grégoire Caurier

Dans le cadre du cours de Webscraping & Data processing de 5ème année en spécialisation DIA à l'ESILV, nous avons travaillé sur un projet d'application utilisant des données venant de scraping de données. 

> Notre problématique est : Quel lien y a-t-il entre la consommation d'énergie et la météo ?

 # Sources de données
 #### 1. Données de consommation d'énergie : Données publiques d'Enedis
Lien : https://data.enedis.fr/explore/dataset/conso-inf36-region/information/
- Données de 2020 (janvier) à 2022 (septembre)
- Pas de une demi heure
- Contient uniquement les souscriptions inférieures à 36 kW/h pour les entreprises (les souscriptions plus importantes se trouvent dans un autre dataset)
- Une ligne pour chaque région, chaque interval de souscription, et chaque catégorie (PRO, RES)
Méthode utilisée : Test d'utilisation de l'API fournie mais limitation à 10 000 lignes de données, donc téléchargement de csv 

#### 2. Données de consommation d'énergie : Données publiques d'Enedis
Lien : https://www.historique-meteo.net/france/
- Possibilité de remonter jusqu'en 2009
- Météo journalière, par région
- Contient la température, l'humidité, les précipitations, l'état du ciel
Méthode utilisée : Scraping web des données utiles pour chaque jour

# Application 
Notre application a été faite sur streamlit, et voici les instructions pour la lancer : 
- exécuter dans le terminal, à l'intérieur du dossier global : 
`streamlit run Accueil.py`
- l'application s'ouvre dans le localhost
- Naviguer entre les pages Accueil et Data Visualisations
	Here's a sentence with a footnote. [^1]

[^1]: This is the footnote.
