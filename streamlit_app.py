import streamlit as st
import pandas as pd
import random
import smtplib
import numpy as np
import os

produits = "produits.xlsx"  
df = pd.read_excel(produits, sheet_name="Produits énergétiques", engine="openpyxl")

left, middle =st.columns([1,3], vertical_alignment="bottom")
left.image("RunBooster(1).png", width=100) 
middle.subheader("Comparateur des différents produits énergétiques du marché")
st.divider()

def load_data():
    df = pd.read_excel("produits.xlsx")  # Remplace par ton fichier
    df["Marque"] = df["Marque"].astype(str)  # Convertir toutes les valeurs en string
    return df

df = load_data()

# Liste des marques uniques avec "Aucune" en option
marques = ["Toutes"] + sorted(df["Marque"].dropna().unique().tolist(), key=str)
# Sélection multiple des marques
selection = st.multiselect("Sélectionne des marques à comparer 👇", marques, default=["Toutes"])
st.write("Choisi 'Toutes' si tu veux toutes les comparer. Sinon, décoche le." )
st.divider()

st.write("Filtre sur les critères suivants: 👇")
filtrer_bio = st.checkbox("Produits Bio")
filtrer_noix = st.checkbox("Sans fruits à coque")
filtrer_lactose = st.checkbox("Sans lactose")
filtrer_gluten = st.checkbox("Sans gluten")
filtrer_dop = st.checkbox("Certification anti-dopage")
filtrer_sel=st.checkbox("Produits salés")
filtrer_caf=st.checkbox("Produits caféinés")
filtrer_nocaf=st.checkbox("Produits sans caféine")
st.divider()
filtrer_barre=st.checkbox("Barres seulement")
filtrer_gel=st.checkbox("Gels seulement")
filtrer_compote=st.checkbox("Compotes seulement")
filtrer_boissons=st.checkbox("Boissons seulement")



# Filtrage par marque
if "Toutes" not in selection:
    df = df[df["Marque"].isin(selection) | (df["Marque"] == "Non communiquée")]

# Appliquer les filtres booléens (Bio, Noix, Lactose, Gluten, DOP)
for critere in ["bio", "dop"]:
    if locals()[f"filtrer_{critere}"]:  # Vérifier si la checkbox est cochée
        df = df[df[critere] == 1]  # Garder uniquement les produits où la valeur est 1
for critere in ["noix", "lactose", "gluten"]:
    if locals()[f"filtrer_{critere}"]:  # Vérifier si la checkbox est cochée
        df = df[df[critere] == 0]  # Garder uniquement les produits où la valeur est 0


if filtrer_barre:
    df=df[(df["Ref"].isin(["BA", "BAS"]))]
if filtrer_boissons:
    df=df[(df["Ref"].isin(["B", "BS"]))]
if filtrer_compote:
    df=df[(df["Ref"].isin(["C", "CS"]))]
if filtrer_gel:
    df=df[(df["Ref"].isin(["G"]))]
if filtrer_sel:
    df=df[(df["Ref"].isin(["CS", "BAS", "BS"]))]
if filtrer_nocaf:
     df = df[df["Caf"] == 0]
if filtrer_caf:
     df = df[df["Caf"] > 0]

# Filtre décroissant
st.divider()
st.write("Clique sur le nom de la colonne pour ordonner les valeurs dans l'ordre croissant ou décroissant")
st.write("La colonne 'Prix' correspond au prix en € pour 1 gramme de glucide dans le produit (€/1g de CHO). Plus la valeur est faible, moins ton ravitaillement sera onéreux.")
st.write("La colonne 'Densité' correspond au grammage de glucide pour 1 gramme de produit  (CHO/1g). Plus la densité est proche de 1, plus le produit est dense en glucide, et donc moins tu embarqueras de poids pour te ravitailler correctement. Sur une course sans assistance, tu pourras ainsi partir le plus léger possible.")
st.write("Pour la catégorie 'Boisson', la colonne 'Sodium' correspond à la quantité de sodium pour le 'poids' de boisson indiqué (Pour 1g de boisson dans la majorité des cas, ou pour plusieurs grammes pour d'autres cas.")
# Affichage des résultats
st.write("### Produits trouvés :")
st.dataframe(
    df[["Marque", "Nom", "prix", "Masse", "Glucide", "densite", "Prot", "Caf", "Sodium"]]
    .rename(columns={
        "prix": "Prix",
        "Masse": "Poids (g)",
        "Glucide": "Glucides (g)",
        "densite": "Densité",
        "Prot": "Protéines (g)",
        "Caf": "Caféine (mg)",
        "Sodium": "Sodium (g)"
    })
)
