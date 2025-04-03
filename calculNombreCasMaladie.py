import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# Connexion à la base de données MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",         # Adaptez le user si nécessaire
    password="",         # Adaptez le password si nécessaire
    database="formulaire"
)

# Requête SQL pour récupérer les diagnostics
query = "SELECT diagnostic FROM dossiers_medical;"
df = pd.read_sql(query, conn)

# Fermer la connexion
conn.close()

# Calculer le nombre de cas par maladie
resultat = df["diagnostic"].value_counts().reset_index()
resultat.columns = ["Maladie", "Nombre de cas"]

# Afficher le résultat
print(resultat)

# Générer un graphique
plt.figure(figsize=(10, 6))
plt.bar(resultat['Maladie'], resultat['Nombre de cas'], color='skyblue')

# Ajouter des labels et un titre
plt.title("Répartition des maladies par nombre de cas")
plt.xlabel("Maladies")
plt.ylabel("Nombre de cas")

# Afficher les labels de manière lisible
plt.xticks(rotation=45, ha='right')

# Afficher le graphique
plt.tight_layout()
plt.show()
