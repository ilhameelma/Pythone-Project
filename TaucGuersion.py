import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Connexion à la base de données
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="formulaire"
)

query = "SELECT etat_guerison FROM guerison"
df_guerison = pd.read_sql(query, conn)

conn.close()

print("Données de la table 'guerison' :")
print(df_guerison)

# Compter les états de guérison
etat_counts = df_guerison["etat_guerison"].value_counts()

# Total des enregistrements
total = len(df_guerison)

# Calcul du taux
taux_gueri = etat_counts.get("Guéri", 0) / total * 100  # Pourcentage de patients guéris
taux_en_cours = etat_counts.get("En Cours", 0) / total * 100  # Pourcentage de patients en cours de traitement
taux_non_gueri = etat_counts.get("Non Guéri", 0) / total * 100  # Pourcentage de patients non guéris

# Affichage des résultats
print(f"Taux de guérison : {taux_gueri:.2f}%")
print(f"Taux de traitement en cours : {taux_en_cours:.2f}%")
print(f"Taux non guéris : {taux_non_gueri:.2f}%")

# Préparer les données pour le graphique
labels = ["Guéri", "En Cours", "Non Guéri"]
taux = [taux_gueri, taux_en_cours, taux_non_gueri]
colors = ["#66ff66", "#ffcc00", "#ff6666"]

# Tracer le graphique en secteurs
plt.figure(figsize=(8, 8))
plt.pie(taux, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
plt.title("Taux de guérison des patients")
plt.axis("equal")  # Assure une forme circulaire

# Afficher le graphique
plt.show()
