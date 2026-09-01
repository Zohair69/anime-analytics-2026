import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration de la page
st.set_page_config(
    page_title="Data Anime Analytics",
    page_icon="🎬",
    layout="wide"
)

# Chargement du jeu de données
@st.cache_data
def load_data():
    df = pd.read_csv("data/anime_dataset_clean.csv")
    return df

df_anime = load_data()

# Navigation latérale
st.sidebar.title("Navigation")
rubrique = st.sidebar.radio(
    "Choisissez une rubrique :",
    [
        "Dashboard Général",
        "Axe 1 : Marché & Formats",
        "Axe 2 : Succès & Popularité",
        "Axe 3 : Genres & Acteurs"
    ]
)

# ---------------------------------------------------------
# DASHBOARD GÉNÉRAL
# ---------------------------------------------------------
if rubrique == "Dashboard Général":
    st.title("📊 Dashboard Général")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Anime", f"{len(df_anime):,}")
    with col2:
        st.metric("Score Moyen", f"{df_anime['score'].mean():.2f}")
    with col3:
        st.metric("Total Membres", f"{int(df_anime['members'].sum()):,}")
    with col4:
        st.metric("Formats Uniques", f"{df_anime['type'].nunique()}")
    
    st.markdown("---")
    st.subheader("Aperçu du jeu de données")
    st.dataframe(df_anime.head(100), use_container_width=True)

# ---------------------------------------------------------
# AXE 1 : MARCHÉ & FORMATS
# ---------------------------------------------------------
elif rubrique == "Axe 1 : Marché & Formats":
    st.title("📌 Axe 1 : Analyse descriptive du marché et des formats")
    
    # 1. Formats de production
    st.subheader("1. Quels formats de production dominent le catalogue ?")
    repartition_types = df_anime['type'].value_counts()
    
    fig1 = px.bar(
        x=repartition_types.values,
        y=repartition_types.index,
        orientation="h",
        title="Répartition des anime par format de production"
    )
    fig1.update_yaxes(categoryorder="total ascending", title_text="Format")
    fig1.update_xaxes(title_text="Nombre d'anime")
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")

    # 2. Évolution au fil des années
    st.subheader("2. Comment le nombre de sorties d'anime a-t-il évolué au fil des années ?")
    
    if 'aired_from' in df_anime.columns:
        # Conversion de aired_from en datetime et extraction de l'année
        df_anime['annee_sortie'] = pd.to_datetime(df_anime['aired_from'], errors='coerce').dt.year
        
        # Compte et tri des sorties par année (filtre jusqu'à 2025)
        sorties_par_annee = df_anime['annee_sortie'].value_counts().sort_index()
        sorties_par_annee = sorties_par_annee[sorties_par_annee.index <= 2025]
        
        fig2 = px.line(
            x=sorties_par_annee.index,
            y=sorties_par_annee.values,
            title="Évolution du nombre de sorties d'anime par année",
            labels={"x": "Année", "y": "Nombre d'anime"}
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("La colonne 'aired_from' n'est pas présente dans le jeu de données.")

    st.markdown("---")

    # 3. Distribution des notes et durées
    st.subheader("3. Comment se distribuent les notes et les durées des anime ?")
    fig3, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].hist(df_anime["score"].dropna(), bins=20)
    axes[0].set_title("Distribution des notes")
    axes[0].set_xlabel("Score")
    axes[0].set_ylabel("Nombre d'anime")

    axes[1].hist(df_anime["episodes"].dropna(), bins=20, range=(0, 100))
    axes[1].set_title("Distribution du nombre d'épisodes (0-100)")
    axes[1].set_xlabel("Episodes")
    axes[1].set_ylabel("Nombre d'anime")

    plt.tight_layout()
    st.pyplot(fig3)

    st.markdown("---")

    # 4. Détection des épisodes atypiques
    st.subheader("4. Détection des anime au nombre d'épisodes atypique")
    df_ep = df_anime.dropna(subset=["episodes"]).copy()
    episodes = df_ep["episodes"].values
    
    if len(episodes) > 0:
        z_scores = (episodes - np.mean(episodes)) / np.std(episodes)
        outliers = df_ep[np.abs(z_scores) > 3]

        st.write(f"**Nombre d'anime atypiques (z-score > 3) :** {len(outliers)}")
        top_outliers = outliers[["title", "episodes"]].sort_values("episodes", ascending=False).head(10)
        st.dataframe(top_outliers, use_container_width=True)

# ---------------------------------------------------------
# AXE 2 : SUCCÈS & POPULARITÉ
# ---------------------------------------------------------
elif rubrique == "Axe 2 : Succès & Popularité":
    st.title("🔥 Axe 2 : Facteurs de succès, popularité et corrélation")
    
    # 1. Matrice de corrélation
    st.subheader("Question 1 : L'engagement du public est-il corrélé avec la note ?")
    num_cols = df_anime.select_dtypes(include=[np.number]).columns
    corr_matrix = df_anime[num_cols].corr()

    fig_corr, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(
        corr_matrix,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        vmin=-1, vmax=1,
        ax=ax
    )
    ax.set_title("Corrélation entre engagement du public et score")
    st.pyplot(fig_corr)

    st.markdown("---")

    # 2. Score par support d'origine
    st.subheader("Question 2 : Le type de source a-t-il un impact sur la note finale ?")
    if 'source' in df_anime.columns:
        score_par_source = df_anime.groupby("source")["score"].mean().sort_values(ascending=False)
        
        fig_source, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(
            x=score_par_source.values,
            y=score_par_source.index,
            palette="Blues_r",
            hue=score_par_source.index,
            legend=False,
            ax=ax
        )
        ax.set_xlabel("Score moyen")
        ax.set_ylabel("Support d'origine")
        ax.set_title("Score moyen par support d'origine")
        plt.tight_layout()
        st.pyplot(fig_source)
    else:
        st.warning("La colonne 'source' n'est pas présente dans le jeu de données.")

    st.markdown("---")

    # 3. Popularité vs Classement
    st.subheader("Question 3 : Le classement reflète-t-il vraiment la popularité ?")
    if 'popularity' in df_anime.columns and 'rank' in df_anime.columns:
        df_rank = df_anime.dropna(subset=['popularity', 'rank']).copy()
        
        # Création des catégories de rangs
        df_rank['categorie_rank'] = pd.qcut(df_rank['rank'], q=5, labels=['Top 20%', '20-40%', '40-60%', '60-80%', '80-100%'])
        df_rank["popularity_inversee"] = df_rank["popularity"].max() - df_rank["popularity"]

        popularity_inv_moyenne = df_rank.groupby("categorie_rank", observed=True)["popularity_inversee"].mean()

        fig_pop, ax = plt.subplots(figsize=(7, 5))
        sns.barplot(x=popularity_inv_moyenne.index, y=popularity_inv_moyenne.values, color="#2b6cb0", ax=ax)
        ax.set_xlabel("Catégorie de classement")
        ax.set_ylabel("Popularité (plus haut = plus populaire)")
        ax.set_title("Popularité selon la catégorie de classement")
        plt.tight_layout()
        st.pyplot(fig_pop)
    else:
        st.warning("Les colonnes 'popularity' ou 'rank' manquent dans le jeu de données.")

# ---------------------------------------------------------
# AXE 3 : GENRES & ACTEURS
# ---------------------------------------------------------
elif rubrique == "Axe 3 : Genres & Acteurs":
    st.title("🎬 Axe 3 : Performance des genres, studios et producteurs")
    
    # Préparation des DataFrames décomposés pour Genres et Studios
    # 1. Genres (sans 'Unknown' / 'Inconnu')
    df_genres = df_anime.copy()
    if 'genres' in df_genres.columns:
        df_genres['genres'] = df_genres['genres'].astype(str)
        df_genres = df_genres.assign(genres=df_genres['genres'].str.split('|')).explode('genres')
        df_genres = df_genres.query("genres not in ['Unknown', 'Inconnu', 'nan', '']")

    # 2. Studios (sans 'Unknown' / 'Inconnu')
    df_studios = df_anime.copy()
    if 'studios' in df_studios.columns:
        df_studios['studios'] = df_studios['studios'].astype(str)
        df_studios = df_studios.assign(studios=df_studios['studios'].str.split('|')).explode('studios')
        df_studios = df_studios.query("studios not in ['Unknown', 'Inconnu', 'nan', '']")

    # 3. Producteurs (sans 'Unknown' / 'Inconnu')
    df_producers = df_anime.copy()
    if 'producers' in df_producers.columns:
        df_producers['producers'] = df_producers['producers'].astype(str)
        df_producers = df_producers.assign(producers=df_producers['producers'].str.split('|')).explode('producers')
        df_producers = df_producers.query("producers not in ['Unknown', 'Inconnu', 'nan', '']")

    # Graphique 1 : Top Genres — Volume vs Score Moyen
    st.subheader("Graphique 1 : Top Genres — Volume vs Score Moyen")
    if 'genres' in df_anime.columns:
        genre_stats = df_genres.groupby('genres').agg(
            count=('mal_id', 'count'),
            mean_score=('score', 'mean')
        ).query('count >= 50').sort_values(by='count', ascending=False).head(15).reset_index()

        genre_stats['score_formatted'] = genre_stats['mean_score'].round(2)
        genre_stats['count_formatted'] = genre_stats['count'].apply(lambda x: f"{x:,}".replace(',', ' '))

        fig_g1 = make_subplots(specs=[[{"secondary_y": True}]])

        fig_g1.add_trace(
            go.Bar(
                x=genre_stats['genres'],
                y=genre_stats['count'],
                name="Volume d'animés",
                marker_color='rgba(31, 119, 180, 0.7)',
                customdata=genre_stats[['count_formatted', 'score_formatted']],
                hovertemplate="<b>Genre : %{x}</b><br>Volume : %{customdata[0]} animés<extra></extra>"
            ),
            secondary_y=False
        )

        fig_g1.add_trace(
            go.Scatter(
                x=genre_stats['genres'],
                y=genre_stats['mean_score'],
                name="Score moyen",
                mode='lines+markers',
                line=dict(color='crimson', width=3),
                marker=dict(size=8),
                customdata=genre_stats[['count_formatted', 'score_formatted']],
                hovertemplate="<b>Genre : %{x}</b><br>Score moyen : %{customdata[1]} / 10<extra></extra>"
            ),
            secondary_y=True
        )

        fig_g1.update_layout(
            title='Top 15 Genres : Volume de Production vs Score Moyen',
            template='plotly_white',
            height=600,
            hovermode="x unified"
        )

        fig_g1.update_yaxes(title_text="Nombre d'animés", secondary_y=False)
        fig_g1.update_yaxes(title_text="Score moyen (/10)", range=[5, 9], tickformat=".2f", secondary_y=True)

        st.plotly_chart(fig_g1, use_container_width=True)

    st.markdown("---")

    # Graphique 2 : Top Studios — Prolificité vs Qualité
    st.subheader("Graphique 2 : Top Studios — Prolificité vs Qualité")
    if 'studios' in df_anime.columns:
        studio_stats = df_studios.groupby('studios').agg(
            count=('mal_id', 'count'),
            mean_score=('score', 'mean'),
            total_members=('members', 'sum')
        ).query('count >= 30').reset_index()

        studio_stats['score_formatted'] = studio_stats['mean_score'].round(2)
        studio_stats['members_formatted'] = studio_stats['total_members'].apply(lambda x: f"{x:,}".replace(',', ' '))

        fig_g2 = px.scatter(
            studio_stats,
            x='count',
            y='mean_score',
            size='total_members',
            size_max=40,
            custom_data=['studios', 'score_formatted', 'members_formatted'],
            title='Performance des Studios : Volume produit vs Score moyen',
            labels={
                'count': "Nombre d'animés produits",
                'mean_score': 'Score Moyen (/10)',
                'total_members': 'Membres cumulés'
            },
            color='mean_score',
            color_continuous_scale='Viridis'
        )

        fig_g2.update_traces(
            hovertemplate="<b>%{customdata[0]}</b><br><br>" +
                          "Nombre d'animés : %{x}<br>" +
                          "Score moyen : %{customdata[1]}<br>" +
                          "Membres cumulés : %{customdata[2]}<extra></extra>"
        )

        fig_g2.update_layout(
            template='plotly_white',
            height=600,
            yaxis=dict(
                autorange=True,
                tickformat=".2f"
            )
        )

        st.plotly_chart(fig_g2, use_container_width=True)

    st.markdown("---")

    # Graphique 3 : Heatmap — Combinations "Studio x Genre"
    st.subheader("Graphique 3 : Heatmap — Les Combinaisons Gagnantes 'Studio x Genre'")
    if 'studios' in df_anime.columns and 'genres' in df_anime.columns:
        top_10_studios = df_studios.groupby('studios')['mal_id'].count().sort_values(ascending=False).head(10).index
        top_10_genres = df_genres.groupby('genres')['mal_id'].count().sort_values(ascending=False).head(10).index

        df_croise = df_studios.assign(genres=df_studios['genres'].str.split('|')).explode('genres')
        df_filtered = df_croise[
            df_croise['studios'].isin(top_10_studios) & 
            df_croise['genres'].isin(top_10_genres)
        ]

        pivot_scores = df_filtered.pivot_table(
            index='studios', columns='genres', values='score', aggfunc='mean'
        ).round(2)

        fig_g3 = px.imshow(
            pivot_scores,
            text_auto='.2f',
            color_continuous_scale='YlGnBu',
            title='Score moyen par combinaison Studio x Genre (Top 10)',
            labels=dict(x='Genre', y='Studio', color='Score moyen'),
            aspect='auto',
        )

        fig_g3.update_traces(
            hovertemplate="<b>Studio :</b> %{y}<br><b>Genre :</b> %{x}<br><b>Score moyen :</b> %{z:.2f} / 10<extra></extra>"
        )

        fig_g3.update_layout(
            template='plotly_white',
            height=600,
            xaxis_title='Genre',
            yaxis_title='Studio',
        )

        st.plotly_chart(fig_g3, use_container_width=True)

    st.markdown("---")

    # Question 4 : Disparité de performance & Valeurs aberrantes (IQR)
    st.subheader("Question 4 : Disparité de performance et valeurs aberrantes par studio")
    if 'studios' in df_anime.columns:
        list_studios = sorted(df_studios['studios'].dropna().unique())
        default_index = list_studios.index('Studio Deen') if 'Studio Deen' in list_studios else 0
        
        studio_target = st.selectbox("Sélectionnez un studio pour l'analyse IQR :", list_studios, index=default_index)

        scores_studio = df_studios.query("studios == @studio_target")['score'].dropna().to_numpy()

        if len(scores_studio) > 0:
            mean_val = np.mean(scores_studio)
            std_val = np.std(scores_studio)
            median_val = np.median(scores_studio)
            q25, q75 = np.percentile(scores_studio, [25, 75])
            iqr = q75 - q25

            threshold_upper = q75 + (1.5 * iqr)
            outliers_high = scores_studio[scores_studio > threshold_upper]

            st.markdown(f"### ANALYSE STATISTIQUE NUMPY : **{studio_target}**")
            col_a, col_b = st.columns(2)
            with col_a:
                st.write(f"- **Moyenne :** {mean_val:.2f}")
                st.write(f"- **Écart-type :** {std_val:.2f}")
                st.write(f"- **Médiane :** {median_val:.2f}")
            with col_b:
                st.write(f"- **Écart Interquartile (IQR) :** {iqr:.2f}")
                st.write(f"- **Seuil de succès exceptionnel (Outlier) :** > {threshold_upper:.2f}")
                st.write(f"- **Nombre de succès exceptionnels isolés :** {len(outliers_high)}")
        else:
            st.info("Aucune donnée de score disponible pour ce studio.")