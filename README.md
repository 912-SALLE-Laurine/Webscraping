# ⛅Projet webscraping : Consommation d'énergie et météo 
Binôme : 👩🏻Laurine Sallé & 👦🏻Grégoire Caurier

Dans le cadre du cours de Webscraping & Data processing de 5ème année en spécialisation DIA à l'ESILV, nous avons travaillé sur un projet d'application utilisant des données venant de scraping de données. 

> Notre problématique est : **Quel lien y a-t-il entre la consommation d'énergie et la météo ?**

L'objectif est de montrer à partir des données, une vue d'ensemble de la consommation électrique en France et par région, et son lien avec la météo

 # Sources de données
 #### 1. Données de consommation d'énergie : Données publiques d'Enedis
Lien : https://data.enedis.fr/explore/dataset/conso-inf36-region/information/
- Données de 2020 (janvier) à 2022 (septembre)
- Pas de une demi heure
- Contient uniquement les souscriptions inférieures à 36 kW/h pour les entreprises (les souscriptions plus importantes se trouvent dans un autre dataset)
- Une ligne pour chaque région, chaque interval de souscription, et chaque catégorie (PRO, RES)

Méthode utilisée : Test d'utilisation de l'API fournie mais limitation à 10 000 lignes de données, donc téléchargement de csv pour réaliser le projet

#### 2. Données de consommation d'énergie : Données publiques d'Enedis
Lien : https://www.historique-meteo.net/france/
- Possibilité de remonter jusqu'en 2009
- Météo journalière, par région
- Contient la température, l'humidité, les précipitations, l'état du ciel

Méthode utilisée : Scraping web des données utiles pour chaque jour

# Application 
Notre application a été faite sur streamlit, et voici les instructions pour la lancer : 
- exécuter dans le terminal, à l'intérieur du dossier global : `streamlit run Accueil.py`
- l'application s'ouvre dans le localhost
- Naviguer entre les pages Accueil et Data Visualisations

Nous avons orgénisé les visualisation, en un zoom temporel, chacune correspondant à une vision temporellement plus précise des données. 
Dans la première visualisation (1er choix dans la sélection "Choisir une visualisation"), les données sont affichées sur la période de 2 ans et demi, puis sur la 2ème, les données sont affichées pour une année, puis un mois et un jour. La dernière visualisation correspond à une vue d'ensemble des régions. 

Des commentaires et interprétations sont directement notées dans l'application. 


# Livrables 
### Code 
Notebooks : 
- *scraping_meteo.ipynb* : scraping des données météo et créaction de datasets
- *traitement_dataset_consommation.ipynb* : A partir de 4 datasets téléchargés depuis le site Enedis, ce notebook effectue un processing et les aggrégation nécessaire à l'obtention des datasets à utiliser pour les visualisation (voir les datasets dans la section datasets). Les datasets originaux ne sont pas sur github, car extrêmement lourds : autour de 4Go au total)

Application Streamlit : 
- *Acceuil.py* : la page d'acceuil
- Dossier *pages*, fichier *01_Data_Visualisations.py* : page de l'application
- Dossier *.streamlit*


### Datasets
- Dossier *meteo_datasets* : *meteo-Auvergne-Rhône-Alpes.csv* et *meteo-Ile-de-France.csv* : météo journalière des régions
- Dossier *regions_datasets_agg* : fichiers d'aggrégation par jour et mois des données des 2 régions
- *conso-inf36-region-agg-month.csv* : consommation sur la France entière aggrégée par mois 
- *conso-inf36-region-agg.csv* : consommation sur la France entière aggrégée par jours 
- *conso-inf36-region-only-some-dates.csv* : consommation par région et par heure seulement sur quelques jours (15 janvier, 15 avril, 15 juillet, 15 octobre)
> Remarque : les choix de jours étant arbitraire (ils ont pour but de représenter chaque saison de l'année), l'étude pourrait être généralisée à plus de jours, voire tous les jours de l'année. Ici la contrainte était le temps de chargement des données, nous avons donc choisi de restreindre afin d'améliorer la rapidité de l'application. 

Nous espérons que le projet vous plaira 😊
