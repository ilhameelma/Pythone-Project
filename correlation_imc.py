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
query = "SELECT imc FROM dossiers_medical;"
df = pd.read_sql(query, conn)

# Fermer la connexion
conn.close()

# Convertir IMC en numérique et gérer les erreurs
df['imc'] = pd.to_numeric(df['imc'], errors='coerce')

# Définition des catégories IMC
def categoriser_imc(imc):
    if imc < 18.5:
        return "Sous-poids"
    elif 18.5 <= imc < 25:
        return "Normal"
    elif 25 <= imc < 30:
        return "Surpoids"
    else:
        return "Obésité"

# Appliquer la classification
df['categorie_imc'] = df['imc'].apply(categoriser_imc)

# Compter le nombre de personnes par catégorie
imc_counts = df['categorie_imc'].value_counts()

# Afficher le tableau des catégories IMC
print("Répartition des personnes selon l'IMC :")
print(imc_counts)

# Tracer un graphique
plt.figure(figsize=(8, 6))
plt.bar(imc_counts.index, imc_counts.values, color=["blue", "green", "orange", "red"])
plt.title("Répartition des personnes selon l'IMC")
plt.xlabel("Catégorie IMC")
plt.ylabel("Nombre de personnes")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
