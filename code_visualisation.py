import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Titre de la page
st.title("Analyse ZEMU comparaison : 2013 vs 2023")

# Chargement des données
df = pd.read_csv("tables/synthese_2023.csv")
df_past = pd.read_csv("tables/synthese_2013.csv")

# Vérifie que les colonnes sont bien alignées
colonnes_disponibles = [col for col in df.columns if col in df_past.columns and col not in ["pole"]]

# Sélection de l’indice
colonne = st.selectbox("Choisissez un indice à comparer :", colonnes_disponibles)

# Récupère la liste complète des pôles/régions
toutes_les_regions = df["pole"].tolist()

# Sélection des régions à afficher
regions_selectionnees = st.multiselect("Choisissez les pôles à comparer :", toutes_les_regions, default=toutes_les_regions)

# Filtrer les DataFrames sur les régions sélectionnées
df_filtre = df[df["pole"].isin(regions_selectionnees)]
df_past_filtre = df_past[df_past["pole"].isin(regions_selectionnees)]

# Positions sur l'axe x
x = np.arange(len(df_filtre))
largeur = 0.35

# Création du graphe
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(x - largeur/2, df_past_filtre[colonne], largeur, label="2013", color="lightgray")
ax.bar(x + largeur/2, df_filtre[colonne], largeur, label="2023", color="cornflowerblue")

# Étiquettes et titres
ax.set_xlabel("Pôles",fontsize=16)
ax.set_ylabel(colonne,fontsize=16)
ax.set_title(f"Comparaison {colonne} : 2013 vs 2023")
ax.set_xticks(x)
ax.set_xticklabels(df_filtre["pole"], rotation=45)
ax.legend()
plt.tight_layout()

# Affichage dans Streamlit
st.pyplot(fig)


# Si la colonne commence par "mxi_", on calcule et affiche un graphe "surface estimée"
if colonne.startswith("mxi_"):
    surface_col = f"surface_estimee_{colonne[4:]}"  # ex: surface_estimee_log

    # Calcul
    df_filtre[surface_col] = df_filtre[colonne] * df_filtre["sp_tot"]
    df_past_filtre[surface_col] = df_past_filtre[colonne] * df_past_filtre["sp_tot"]

    # Affichage
    st.subheader(f"Superficie : {colonne[4:]} (m²)")

    fig2, ax2 = plt.subplots(figsize=(12, 6))
    ax2.bar(x - largeur/2, df_past_filtre[surface_col], largeur, label="2013", color="lightgray")
    ax2.bar(x + largeur/2, df_filtre[surface_col], largeur, label="2023", color="seagreen")
    ax2.set_xlabel("Pôles", fontsize=16)
    ax2.set_ylabel(f"Superficie {colonne[4:]} (m²)", fontsize=16)
    ax2.set_title("2013 vs 2023", fontsize=18)
    ax2.set_xticks(x)
    ax2.set_xticklabels(df_filtre["pole"], rotation=45)
    ax2.legend()
    plt.tight_layout()
    st.pyplot(fig2)