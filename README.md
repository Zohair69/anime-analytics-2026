# 🎬 Data Anime Analytics — Application Streamlit

Bienvenue sur le projet **Data Anime Analytics**. Cette application web interactive développée avec **Streamlit** permet de visualiser et d'analyser un jeu de données sur les animes, en mettant en évidence l'évolution du marché, les facteurs de succès et la performance des genres/studios.

🔗 **Lien de l'application en ligne :** https://dataanimesteamlit-k5wowxvwreqoaukveesmbw.streamlit.app

---

## 📌 Fonctionnalités & Structure de l'Analyse

L'application est structurée en plusieurs rubriques accessibles depuis le menu latéral :

*   **📊 Dashboard Général :** Aperçu global du dataset avec des métriques clés (score moyen, nombre d'animes, membres cumulés) et la table de données interactive.
*   **📌 Axe 1 : Analyse descriptive du marché et des formats :**
    *   Répartition des animes par format de production (TV, Movie, OVA...).
    *   Évolution historique des sorties d'animes par année (basée sur la date de début de diffusion).
    *   Distribution des notes et du nombre d'épisodes (visualisation Matplotlib).
    *   Détection des séries aux durées atypiques (analyse statistique par Z-Score).
*   **🔥 Axe 2 : Facteurs de succès, popularité et corrélation :**
    *   Matrice de corrélation entre les métriques d'engagement et le score (Seaborn Heatmap).
    *   Impact du support d'origine (manga, light novel, etc.) sur la note finale.
    *   Analyse de la popularité selon la catégorie de classement.
*   **🎬 Axe 3 : Performance des genres, studios et producteurs :**
    *   **Top Genres :** Comparaison entre volume de production et score moyen (graphique Plotly double axe Y).
    *   **Performance des Studios :** Prolificité vs Qualité vs Audience cumulée.
    *   **Combinaisons Gagnantes (Studio x Genre) :** Heatmap croisée montrant les scores moyens par association.
    *   **Analyse de Variabilité (NumPy) :** Calcul de la médiane, de l'IQR et détection des succès exceptionnels (Outliers) par studio.

---

## 🛠️ Technologies Utilisées

*   **Langage :** Python
*   **Framework Web :** Streamlit
*   **Traitement de données :** Pandas, NumPy
*   **Data Visualization :** Plotly Express / Graph Objects, Matplotlib, Seaborn

---

## 📂 Structure du Projet

```
Data_Anime_Steamlit/
│
├── data/
│   └── anime_dataset_clean.csv      # Jeu de données nettoyé
│
├── src/
│   └── app.py                       # Fichier principal Streamlit
│
├── .gitignore                       # Fichiers et dossiers à ignorer par Git
├── README.md                        # Documentation du projet
└── requirements.txt                 # Dépendances du projet pour le déploiement
