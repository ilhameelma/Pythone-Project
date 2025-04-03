import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 🔹 Connexion à la base de données MySQL
conn = mysql.connector.connect(
    host="localhost",
            user="root",         # Adaptez le user si nécessaire
            password="",         # Adaptez le password si nécessaire
            database="formulaire"
)

# 🔹 Création du curseur
cursor = conn.cursor()

# 🔹 Récupération des données
query = "SELECT date_consultation, diagnostic FROM dossiers_medical"
cursor.execute(query)

# 🔹 Chargement des données dans Pandas
df = pd.DataFrame(cursor.fetchall(), columns=['date_consultation', 'diagnostic'])

# 🔹 Fermeture de la connexion
cursor.close()
conn.close()

# 📌 Vérifier les données chargées
print("🔍 Aperçu des données avant traitement :")
print(df.head())

# 🔹 Suppression des valeurs nulles dans `date_consultation`
df = df.dropna(subset=['date_consultation'])

# 🔹 Conversion en datetime (ignorer erreurs si problème de format)
df['date_consultation'] = pd.to_datetime(df['date_consultation'], errors='coerce')

# 📌 Vérification après nettoyage
print("✅ Données après suppression des valeurs nulles et conversion des dates :")
print(df.info())

# 🔹 Grouper par mois et maladie
df_grouped = df.groupby([df['date_consultation'].dt.to_period('M'), 'diagnostic']).size().unstack().fillna(0)

# 🔹 Affichage des tendances des maladies
plt.figure(figsize=(12, 6))
df_grouped.plot(kind='line', marker='o', figsize=(12, 6), title="Tendance des maladies par mois")
plt.xlabel("Date (mois)")
plt.ylabel("Nombre de cas")
plt.grid(True)
plt.legend(title="Maladies")

# 🔹 Forcer l'affichage du graphique
plt.show(block=True)

