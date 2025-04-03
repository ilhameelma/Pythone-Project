import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

# Connexion à la base MySQL
conn = mysql.connector.connect(
    host="localhost",  # Modifier si nécessaire
    user="root",       # Modifier si nécessaire
    password="",       # Modifier si nécessaire
    database="formulaire"  # Nom de ta base de données
)
cursor = conn.cursor()

# Requête SQL pour récupérer les données
query = """
SELECT dm.diagnostic, u.sexe
FROM dossiers_medical dm
JOIN utilisateurs u ON dm.utilisateur_id = u.id
"""
cursor.execute(query)

# Charger les données dans un DataFrame Pandas
df = pd.DataFrame(cursor.fetchall(), columns=['diagnostic', 'sexe'])

# Fermer la connexion
cursor.close()
conn.close()

# Vérifier les données
print(df.head())

# Supprimer les valeurs manquantes
df_clean = df.dropna()

# Compter le nombre d'hommes et de femmes par maladie
repartition = df_clean.groupby(['diagnostic', 'sexe']).size().unstack()

# Afficher le tableau
print(repartition)

# Tracer un graphique
repartition.plot(kind='bar', figsize=(12, 6), stacked=True)
plt.title("Répartition hommes/femmes par maladie")
plt.xlabel("Maladies")
plt.ylabel("Nombre de cas")
plt.legend(["Féminin", "Masculin"])
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
