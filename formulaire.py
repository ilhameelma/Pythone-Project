from tkinter import *
from tkinter import filedialog, messagebox
from tkcalendar import DateEntry 
import mysql.connector 
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector
import re
from tkinter import filedialog
def supprimer_container:
    window = Tk()
    window.title("Suppression Utilisateur")

    # Label et champ de saisie
    label_supprimer = Label(window, text="Donner l'ID de l'utilisateur à supprimer :")
    label_supprimer.pack()
    entry_supprimer = Entry(window)
    entry_supprimer.pack()

    # Fonction pour la connexion à la base de données
    def get_connection():
        return mysql.connector.connect(
            host="localhost",
            user="root",  # Modifier si nécessaire
            password="",  # Modifier si nécessaire
            database="formulaire"
        )

    # Fonction pour supprimer un utilisateur et son dossier médical
    def supprimer_utilisateur():
        user_id = entry_supprimer.get().strip()

        if not user_id.isdigit():
            messagebox.showerror("Erreur", "L'ID doit être un nombre valide.")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Suppression dans les tables avec contrainte d'intégrité
            cursor.execute("DELETE FROM dossiers_medical WHERE utilisateur_id = %s", (user_id,))
            cursor.execute("DELETE FROM utilisateurs WHERE id = %s", (user_id,))

            conn.commit()
            messagebox.showinfo("Succès", "Utilisateur supprimé avec succès.")

        except mysql.connector.Error as e:
            messagebox.showerror("Erreur", f"Erreur MySQL : {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    # Bouton de suppression
    btn_supprimer = Button(window, text="Supprimer", command=supprimer_utilisateur)
    btn_supprimer.pack()

    # Lancer l'application
    window.mainloop()
# Connexion à MySQL (à la racine de MySQL sans spécifier de base de données)
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # Changez si nécessaire
    password=""   # Changez si nécessaire
)
cursor = conn.cursor()

# Créer la base de données si elle n'existe pas
cursor.execute("CREATE DATABASE IF NOT EXISTS medical_db")
conn.commit()

# Connexion à la base de données spécifique
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # Changez si nécessaire
    password="",  # Changez si nécessaire
    database="medical_db"
)
cursor = conn.cursor()

# Création de la table si elle n'existe pas
cursor.execute('''CREATE TABLE IF NOT EXISTS dossiers_medical (
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur_id INT,  
    antecedents_familiaux TEXT,
    antecedents_personnels TEXT,
    interventions TEXT,
    vaccinations TEXT,
    traitements TEXT,
    date_consultation DATE,
    motif TEXT,
    symptomes TEXT,
    diagnostic TEXT,
    medecin TEXT,
    temperature FLOAT,
    tension TEXT,
    imc TEXT,
    analyses TEXT,
    medicaments TEXT,
    conseils TEXT,
    prochain_rdv DATE,
    consentement TEXT,
    signature_medecin TEXT,
    signature_patient TEXT,
    fichier TEXT,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id)
)''')
conn.commit()


# Fonction pour sélectionner un fichier médical
def ajouter_fichier():
    fichier_path = filedialog.askopenfilename(title="Sélectionner un fichier médical",
                                              filetypes=[("Tous les fichiers", "."), 
                                                         ("PDF", "*.pdf"), 
                                                         ("Images", ".jpg;.png"),
                                                         ("Documents", ".docx;.txt")])
    if fichier_path:
        fichier_label.config(text=f"Fichier sélectionné: {fichier_path}")

# Fonction pour enregistrer les données dans la base
def afficher_entry(section, index):
    if sections[section]["variables"][index].get():  
        sections[section]["entries"][index].pack(side="left", padx=5)  # Afficher Entry
    else:
        sections[section]["entries"][index].pack_forget()  # Masquer Entry
def submit():
    try:
        data = {section: {} for section in sections.keys()}
        for section, content in sections.items():
            for i, var in enumerate(content["variables"]):
                if var.get():
                    data[section][content["elements"][i]] = content["entries"][i].get()

        fichier = fichier_label.cget("text").replace("Fichier sélectionné: ", "")

        # Récupérer l'ID de l'utilisateur (en supposant que l'utilisateur a déjà été inscrit)
        cursor.execute("SELECT id FROM utilisateurs WHERE email = %s", (data["Informations sur la Consultation"].get("Email", ""),))
        utilisateur_id = cursor.fetchone()[0]  # Récupère l'ID de l'utilisateur

        cursor.execute('''INSERT INTO dossiers_medical (
            utilisateur_id, antecedents_familiaux, antecedents_personnels, interventions, vaccinations, traitements,
            date_consultation, motif, symptomes, diagnostic, medecin,
            temperature, tension, imc, analyses,
            medicaments, conseils, prochain_rdv,
            consentement, signature_medecin, signature_patient,
            fichier
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
        (
            utilisateur_id,
            data["Antécédents Médicaux"].get("Antécédents familiaux", ""),
            data["Antécédents Médicaux"].get("Antécédents personnels", ""),
            data["Antécédents Médicaux"].get("Interventions chirurgicales passées", ""),
            data["Antécédents Médicaux"].get("Vaccinations", ""),
            data["Antécédents Médicaux"].get("Traitements en cours", ""),
            data["Informations sur la Consultation"].get("Date de la consultation", ""),
            data["Informations sur la Consultation"].get("Motif de la consultation", ""),
            data["Informations sur la Consultation"].get("Symptômes", ""),
            data["Informations sur la Consultation"].get("Diagnostic", ""),
            data["Informations sur la Consultation"].get("Médecin responsable", ""),
            data["Tests Médicaux"].get("Température corporelle", ""),
            data["Tests Médicaux"].get("Tension artérielle", ""),
            data["Tests Médicaux"].get("Poids et taille (IMC)", ""),
            data["Tests Médicaux"].get("Résultats d’analyses", ""),
            data["Traitement & Prescription Médicale"].get("Médicaments prescrits", ""),
            data["Traitement & Prescription Médicale"].get("Conseils et recommandations médicales", ""),
            data["Traitement & Prescription Médicale"].get("Prochain rendez-vous", ""),
            data["Consentements & Signature"].get("Consentement du patient", ""),
            data["Consentements & Signature"].get("Signature du médecin", ""),
            data["Consentements & Signature"].get("Signature du patient", ""),
            fichier
        ))
        conn.commit()
        messagebox.showinfo("Succès", "Les données ont été enregistrées avec succès !")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")


# Création de la fenêtre principale
window = Tk()
window.title("Formulaire Médical")
window.geometry("700x750")

# Centrage de la fenêtre
window_width, window_height = 700, 750
screen_width, screen_height = window.winfo_screenwidth(), window.winfo_screenheight()
x, y = (screen_width // 2) - (window_width // 2), (screen_height // 2) - (window_height // 2)
window.geometry(f'{window_width}x{window_height}+{x}+{y}')

# Cadre principal
main_frame = LabelFrame(window, text="Formulaire Médical", font=("Arial", 14, "bold"), padx=10, pady=10, bd=2, relief="ridge", fg="blue")
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

# Canvas + Scrollbar
canvas = Canvas(main_frame)
scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas)
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Définition des sections
sections = {
    "Antécédents Médicaux": [
        "Antécédents familiaux", "Antécédents personnels",
        "Interventions chirurgicales passées", "Vaccinations", "Traitements en cours"
    ],
    "Informations sur la Consultation": [
        "Date de la consultation", "Motif de la consultation", "Symptômes",
        "Diagnostic", "Médecin responsable"
    ],
    "Tests Médicaux": [
        "Température corporelle", "Tension artérielle", "Poids et taille (IMC)",
        "Résultats d’analyses"
    ],
    "Traitement & Prescription Médicale": [
        "Médicaments prescrits", "Conseils et recommandations médicales",
        "Prochain rendez-vous"
    ],
    "Consentements & Signature": [
        "Consentement du patient", "Signature du médecin", "Signature du patient"
    ]
}

# Stockage des variables et entries
for section, elements in sections.items():
    section_frame = LabelFrame(scrollable_frame, text=section, font=("Arial", 12, "bold"), padx=10, pady=10, bd=1, relief="solid", fg="blue")
    section_frame.pack(pady=10, fill="x")

    variables = []
    entries = []

    for i, element in enumerate(elements):
        entry_frame = Frame(section_frame)
        entry_frame.pack(pady=5, anchor="w")

        var = BooleanVar()
        chk = Checkbutton(entry_frame, text=element, variable=var, command=lambda s=section, idx=i: afficher_entry(s, idx))
        chk.pack(side="left")

        if section == "Informations sur la Consultation" and element == "Date de la consultation":
            entry = DateEntry(entry_frame, width=15, background="blue", foreground="white", date_pattern="yyyy-mm-dd")
        else:
            entry = Entry(entry_frame, width=40)

        entry.pack_forget()  # Masquer tous les champs au début
        entries.append(entry)
        variables.append(var)

    sections[section] = {"elements": elements, "variables": variables, "entries": entries}

# Section Ajout Fichier
fichier_frame = LabelFrame(scrollable_frame, text="Ajout de Fichier Médical", font=("Arial", 12, "bold"), padx=10, pady=10, bd=1, relief="solid")
fichier_frame.pack(pady=20, padx=10, fill="x")

ajouter_btn = Button(fichier_frame, text="Ajouter un fichier médical", command=ajouter_fichier, bg="blue", fg="white")
ajouter_btn.pack(pady=5)

fichier_label = Label(fichier_frame, text="", wraplength=500, fg="black")
fichier_label.pack(pady=5)

submit_btn = Button(scrollable_frame, text="Soumettre", command=submit, bg="green", fg="white")
submit_btn.pack(pady=20)

window.mainloop()

def fermer_connexion():
    cursor.close()
    conn.close()

window.protocol("WM_DELETE_WINDOW", fermer_connexion)