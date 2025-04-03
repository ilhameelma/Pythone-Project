import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
# Connexion à la base de données
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="formulaire" 
)

# Extraction des données nécessaires
query_utilisateurs = "SELECT id, date_naissance FROM utilisateurs"
query_dossiers = "SELECT utilisateur_id, diagnostic FROM dossiers_medical"

# Charger les données dans des DataFrames Pandas
df_utilisateurs = pd.read_sql(query_utilisateurs, conn)
df_dossiers = pd.read_sql(query_dossiers, conn)

conn.close()


# Calculer l'âge à partir de la date de naissance
current_year = datetime.now().year
df_utilisateurs["age"] = df_utilisateurs["date_naissance"].apply(lambda x: current_year - pd.to_datetime(x).year)

print("\nDonnées Utilisateurs avec Âge :")
print(df_utilisateurs)

# Fusion des données utilisateurs et dossiers médicaux
df_combined = pd.merge(df_utilisateurs, df_dossiers, left_on="id", right_on="utilisateur_id")

print("\nDonnées Fusionnées :")
print(df_combined)

# Définir les tranches d'âge
conditions = [
    (df_combined["age"] < 18),
    (df_combined["age"] >= 18) & (df_combined["age"] <= 40),
    (df_combined["age"] > 40)
]
choices = ["<18", "18-40", ">40"]

df_combined["groupe_age"] = np.select(conditions, choices, default="Inconnu")

print("\nDonnées avec Groupes d'Âge :")
print(df_combined)




# Regrouper les données par groupe d'âge et diagnostic
grouped_data = df_combined.groupby(["groupe_age", "diagnostic"]).size().reset_index(name="count")

# Préparer les données pour le graphique
grouped_age = grouped_data["groupe_age"].unique()

# Tracer un graphique à barres horizontales
for age_group in grouped_age:
    subset = grouped_data[grouped_data["groupe_age"] == age_group]
    plt.barh(subset["diagnostic"], subset["count"], label=f"Groupe {age_group}")

# Personnaliser le graphique
plt.title("Répartition des diagnostics par tranche d'âge")
plt.xlabel("Nombre de cas")
plt.ylabel("Diagnostic")
plt.legend(title="Tranches d'âge")
plt.tight_layout()

# Afficher le graphique
plt.show()


