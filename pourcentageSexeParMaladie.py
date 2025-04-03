import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

# Connexion à la base de données MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="formulaire"
)

# Charger les données depuis la base
query = "SELECT sexe FROM dossiers_medical INNER JOIN utilisateurs ON dossiers_medical.utilisateur_id = utilisateurs.id;"
df = pd.read_sql(query, conn)

# Fermer la connexion
conn.close()

# Supprimer les valeurs manquantes
df_clean = df.dropna()

# Compter le nombre de cas par sexe
sexe_counts = df_clean["sexe"].value_counts()

# Calculer le pourcentage total
pourcentage_sexe = (sexe_counts / sexe_counts.sum()) * 100

# Afficher le tableau des pourcentages
print("Pourcentage total des cas par sexe :")
print(pourcentage_sexe)

# Tracer un graphique
plt.figure(figsize=(6, 6))
plt.pie(pourcentage_sexe, labels=pourcentage_sexe.index, autopct='%1.1f%%', colors=["blue", "pink"], startangle=90)
plt.title("Répartition des maladies par sexe")
plt.show()

