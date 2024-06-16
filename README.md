# AirBnB : Facteurs influençant sur les prix <br><br>
<p align="center">
    <img src="airbnb.png" alt="airbnb" width="180" height="180">
</p>
# 1. Contexte et objectifs du projet
<p>Dans le secteur de l'hébergement touristique, la tarification est cruciale pour la compétitivité et la rentabilité. Sur des plateformes telles qu'Airbnb, comprendre les facteurs influençant les prix est essentiel tant pour les hôtes que pour les voyageurs. Cette étude examine plusieurs éléments, tels que la localisation, les caractéristiques des logements et les évaluations, qui impactent les tarifs des hébergements Airbnb. En fournissant des insights précieux, notre objectif est de guider les décisions des acteurs du marché.</p>
<p>En comprenant mieux ces dynamiques, nous espérons offrir une perspective éclairante sur la manière dont les prix sont fixés sur Airbnb. Cela permettra aux acteurs du marché de prendre des décisions plus informées pour maximiser leur satisfaction et leurs bénéfices.</p>
<p>Le projet vise à développer un système de web scraping pour collecter des données sur les prix des hébergements Airbnb, ainsi que les facteurs qui influent sur ces prix, notamment les évaluations, le nombre de chambres, le pays, la région, le type de logement et la capacité d'accueil en termes de personnes. L'objectif principal est d'analyser ces données pour identifier les tendances et les relations entre les différents facteurs et les prix, avec et sans remise.</p>

# 2. Données (sources, quantité, éventuel pré-traitement, description)
<p>Les données proviennent du site Airbnb. J'ai scrappé les données des pays suivants : Espagne, Allemagne, Autriche, Belgique, Suisse, France, Italie, et Portugal, pour la période du 31/07/2024 au 31/08/2024. Le dataset initial comprend 1189 lignes incluant les informations suivantes :
<li>Price
<li>old_price
<li>type
<li>pays
<li>region 
<li>title
<li>rating
<li>voyageurs
<li>rooms
<li>bed
<li>bathroom
<li>periode_start
<li>periode_end
</p>
<p>Un pré-traitement a été effectué pour nettoyer les données et corriger les incohérences, ce qui a abouti à un dataset propre de 754 lignes. Les étapes de nettoyage ont inclus :
<li>La suppression des données erronées
<li>La suppression des lignes contenant des données manquantes
<li>La suppression de la colonne Title qui ne sera pas utilisée dans notre analyse
</p>
<p>Les données scrappées étaient initialement au format objet. Après nettoyage, les nouveaux formats sont :
<li>float pour Prix, old_price et Rating
<li>int pour voyageurs, rooms, bed, et bathroom
<li>string pour Type, pays, et region
<li>datetime pour period_start et period_end

# 3. État de l'art
<p>La tarification des hébergements sur Airbnb a été largement étudiée. Des chercheurs ont utilisé divers modèles de machine learning pour prédire les prix des locations. Par exemple, une étude a développé un modèle de prédiction des prix en utilisant des spécifications de propriété, des informations sur les propriétaires et des avis clients, en utilisant des techniques de régression et d'analyse de sentiments pour améliorer la précision des prédictions<a href="https://www.mdpi.com/2071-1050/15/17/13159"> <strong>MDPI</strong></a></p>
<p>Plusieurs études ont employé des algorithmes de data mining pour examiner l'impact économique d'Airbnb sur les villes, prédire les destinations de réservation des utilisateurs et analyser les préférences des utilisateurs basées sur les avis. Des méthodes telles que la régression Lasso et Ridge ont été appliquées, et l'analyse de sentiments a été utilisée pour extraire des caractéristiques pertinentes des avis clients​ <a href="https://www.mdpi.com/2071-1050/15/17/13159"> <strong>MDPI</strong></a></p>
<p>Notre projet se distingue en ciblant une période spécifique (31/07/2024 au 31/08/2024) et en analysant les facteurs de corrélation avec les prix des hébergements Airbnb dans plusieurs pays européens. En intégrant des données récentes et en utilisant des techniques de nettoyage de données rigoureuses, notre étude vise à fournir des insights plus précis et actuels pour aider les hôtes et les voyageurs à mieux comprendre les dynamiques de tarification sur Airbnb.</p>

# 4. Conception / Cas d'utilisation / Architecture
## Conception générale
<p>Notre projet de web scraping et d'analyse des prix des hébergements Airbnb se structure autour de plusieurs étapes clés :
<ol>
    <li><strong>Collecte de données :</strong> Utilisation de scripts de web scraping pour extraire les informations pertinentes des annonces Airbnb.
    <li><strong>Pré-traitement des données :</strong> Nettoyage et transformation des données brutes pour les rendre exploitables (suppression des valeurs manquantes, conversion des types de données, etc.).
    <li><strong>Analyse des données : </strong>Utilisation de techniques statistiques et de machine learning pour identifier les facteurs influençant les prix.
    <li><strong>Visualisation des résultats :</strong> Création de visualisations pour représenter les résultats de manière compréhensible et informative.
</ol>

## Cas d'utilisation 
<ol>
<li>Cas d'utilisation principal - Utilisateur : Analyste de données
    <ul>
        <li><strong>Scénario :</strong> L'analyste souhaite comprendre les facteurs influençant les prix des hébergements Airbnb.
        <li><strong>Etapes:</strong>
            <ol>
                <li>Exécuter le script de web scraping pour collecter les données.
                <li>Charger les données dans un outil d'analyse.
                <li>Appliquer des techniques de pré-traitement pour nettoyer les données.
                <li>Effectuer une analyse statistique pour identifier les corrélations entre les différentes variables et les prix.
                <li>Visualiser les résultats sous forme de graphiques et de tableaux.
            </ol>
    </ul>
<li>Cas d'utilisation secondaire - Utilisateur : Propriétaire Airbnb
    <ul>
        <li><strong>Scénario :</strong>  Un propriétaire souhaite ajuster le prix de son hébergement en fonction des tendances du marché.
        <li><strong>Etapes:</strong>
            <ol>
                <li>Consulter les visualisations des analyses effectuées.
                <li>Identifier les caractéristiques de son propre hébergement (localisation, nombre de chambres, etc.).
                <li>Ajuster les prix en fonction des insights obtenus.
            </ol>
    </ul>
</li>




## Description des Composants Principaux

<ol>
    <li>collecte de données :
        <ul>
            <li><strong>Outils :</strong> Bibliothèques de scraping web (par exemple, BeautifulSoup).
            <li><strong>Fonctionnalités : </strong>Extraction des informations pertinentes depuis le site web d'Airbnb.
        </ul>
    <li>Pré-traitement des données :    
        <ul>
            <li><strong>Outils :</strong>  Pandas pour la manipulation des données.
            <li><strong>Fonctionnalités : </strong>Nettoyage des données, gestion des valeurs manquantes, conversion des types de données.
        </ul>
    <li>Analyse des données  :    
        <ul>
            <li><strong>Outils :</strong>  Scikit-learn pour le machine learning, bibliothèques statistiques.
            <li><strong>Fonctionnalités : </strong>Analyse des corrélations, modélisation prédictive.
        </ul>
    <li>Visualisation :    
        <ul>
            <li><strong>Outils :</strong>  Matplotlib, Seaborn pour la création de graphiques..
            <li><strong>Fonctionnalités : </strong>Génération de visualisations claires et informatives des résultats d'analyse.
        </ul>
</ol>

# 5. Fonctionnalités
## Fonctionnalité 1 : Ouvrire les pages Airbnb dans un navigateur
<ul>
    <li>L'application doit être capable d'ouvrir les pages Airbnb dans un navigateur web tel que 
Google Chrome ou Mozilla Firefox. 
    <li>Elle doit permettre à l'utilisateur de spécifier l'URL de la page Airbnb ou de fournir des 
critères de recherche pour trouver automatiquement les pages à ouvrir
</ul>

## Fonctionnalité 2 : Conditions de Chargement de Page
<ul>
    <li>Avant de procéder au scraping des données, l'application doit s'assurer que la page 
Airbnb est entièrement chargée pour éviter les erreurs de scraping dues à des données 
manquantes 
    <li>Des conditions doivent être mises en place pour vérifier que les éléments essentiels de 
la page, tels que les prix et les évaluations, sont disponibles et accessibles avant de 
poursuivre le processus de scraping. 
</ul>

## Fonctionnalité 3 : Simulation de Clics sur la Page 
<ul>
    <li>L'application doit être capable de simuler des clics sur la page Airbnb si nécessaire, par 
exemple pour charger davantage de résultats ou pour afficher des informations 
supplémentaires.
    <li>Cette fonctionnalité peut être utilisée pour naviguer entre les différentes sections de la 
page ou pour accéder à des détails spécifiques sur les hébergements.
</ul>

## Fonctionnalité 4 : Scraping des Données
<ul>
    <lil>Une fois que la page Airbnb est correctement chargée, l'application doit extraire les 
données pertinentes telles que les prix, les évaluations, le nombre de chambres, etc., en 
utilisant des techniques de scraping web. 
    <li>Elle doit être capable de récupérer les informations à partir des balises HTML 
appropriées sur la page et de les stocker pour le traitement ultérieur. 
</ul>

## Fonctionnalité 5 : Enregistrement des Données sous Forme CSV
<ul>
    <li>Après avoir extrait les données, l'application doit les enregistrer dans un fichier CSV pour 
un accès et une analyse ultérieure. 
    <li>Le fichier CSV doit être organisé de manière à ce que les données soient facilement 
utilisables pour le traitement et l'analyse.
</ul>

## Fonctionnalité 6 : Data Wrangling (Nettoyage des Données)
<ul>
    <li>Avant d'analyser les données, l'application doit effectuer des opérations de nettoyage 
pour éliminer les valeurs aberrantes, les doublons et les données manquantes. 
</ul>

## Fonctionnalité 7 : Analyse des Données 
<ul>
    <li>Enfin, l'application peut fournir des fonctionnalités d'analyse des données pour 
identifier des tendances, des corrélations ou des insights intéressants à partir des 
données extraites.
    <li>Cela peut inclure des visualisations graphiques, des statistiques descriptives ou 
d'autres techniques d'analyse de données. 
</ul>

# 6. Techniques, algorithmes et outils utilisés 
<ul>
    <li>Prédiction des Prix et Rating
        <ul>
            <li>Cette étape consiste à utiliser RapidMiner pour développer, évaluer et comparer des modèles de prédiction des prix et des ratings d'accommodations. Les techniques employées incluent la régression linéaire et la forêt aléatoire. Le processus couvre plusieurs étapes :</li>
            <ol>
                <li>Préparation des données : Nettoyage et transformation pour l'analyse.</li>
                <li>Modélisation et prédiction : Construction et entraînement des modèles de régression linéaire et de forêt aléatoire.</li>
                <li>Évaluation des modèles : Validation croisée et séparation des données pour évaluer la précision et la robustesse des modèles.</li>
            </ol>
        </ul>
    </li>
    <li>Clustering
        <ul>
            <li>Le clustering des régions est effectué en fonction de leur réduction de prix moyenne. Les étapes incluent :</li>
            <ol>
                <li>Préparation des données : Calcul des réductions de prix et normalisation.</li>
                <li>Clustering K-Means : Application de l'algorithme avec trois clusters.</li>
                <li>Visualisation sur carte : Utilisation de folium pour créer une carte interactive des clusters.</li>
            </ol>
        </ul>
    </li>
    <li>Visualisation avec Streamlit
        <ul>
            <li>Une interface interactive est développée avec Streamlit pour visualiser les résultats du clustering et des modèles de prédiction. Les éléments clés de l'interface sont :</li>
            <ol>
                <li>Carte interactive : Présentation des clusters de réduction de prix par région.</li>
                <li>Graphiques de modèles de prédiction : Visualisation des performances des modèles de régression linéaire et de forêt aléatoire.</li>
            </ol>
            <li>Cette interface permet une analyse approfondie et interactive des données, facilitant la prise de décision basée sur les résultats des modèles et du clustering.</li>
        </ul>
    </li>
</ul>



# 7. Planification, organisation et suivi répartition du travail (diagramme de Gantt)

![alt text](<Diagramme de Gantt.PNG>)

# Conclusion / Travail futur
<p>Ce projet de web mining sur les prix des hébergements Airbnb a permis de mettre en lumière les principaux facteurs influençant la tarification, tels que la localisation, les caractéristiques des logements, et les évaluations des clients. Grâce à une méthodologie rigoureuse de collecte, de nettoyage et d'analyse des données, nous avons identifié des tendances et des corrélations significatives qui peuvent guider les hôtes dans l'optimisation de leurs prix. À l'avenir, il serait intéressant d'intégrer des techniques de machine learning plus avancées, comme les réseaux de neurones profonds, pour affiner les prédictions de prix et explorer l'impact des événements locaux ou saisonniers sur la demande. De plus, la création d'une interface utilisateur interactive via des outils comme Streamlit pourrait faciliter l'accès aux analyses et recommandations pour les hôtes, leur permettant d'ajuster en temps réel leurs stratégies de tarification pour maximiser leurs revenus et améliorer la satisfaction des voyageurs.</p>



