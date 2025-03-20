from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector
import re
from tkinter import filedialog, messagebox


# Fonction de connexion à MySQL
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Changez si nécessaire
        password="",   # Changez si nécessaire
        database="formulaire"  # Base de données où les informations seront stockées
    )




def formulaire_medicale(window, utilisateur_id):
    conn = get_connection()
    cursor = conn.cursor()

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

    def ajouter_fichier():
        fichier_path = filedialog.askopenfilename(title="Sélectionner un fichier médical",
                                                  filetypes=[("Tous les fichiers", "."), 
                                                            ("PDF", "*.pdf"), 
                                                            ("Images", ".jpg;.png"),
                                                            ("Documents", ".docx;.txt")])
        if fichier_path:
            fichier_label.config(text=f"Fichier sélectionné: {fichier_path}")

    def afficher_entry(section, index):
        if sections[section]["variables"][index].get():
            sections[section]["entries"][index].pack(side="left", padx=5)
        else:
            sections[section]["entries"][index].pack_forget()

    def submit():
     try:
        # Récupérer les données à partir des sections
        data = {section: {} for section in sections.keys()}
        for section, content in sections.items():
            for i, var in enumerate(content["variables"]):
                if var.get():
                    data[section][content["elements"][i]] = content["entries"][i].get()

        # Récupérer le chemin du fichier sélectionné
        fichier = fichier_label.cget("text").replace("Fichier sélectionné: ", "")

        # Liste des champs et valeurs à insérer
        champs_valeurs = [
            ("utilisateur_id", utilisateur_id),
            ("antecedents_familiaux", data["Antécédents Médicaux"].get("Antécédents familiaux", "")),
            ("antecedents_personnels", data["Antécédents Médicaux"].get("Antécédents personnels", "")),
            ("interventions", data["Antécédents Médicaux"].get("Interventions chirurgicales passées", "")),
            ("vaccinations", data["Antécédents Médicaux"].get("Vaccinations", "")),
            ("traitements", data["Antécédents Médicaux"].get("Traitements en cours", "")),
            ("date_consultation", data["Informations sur la Consultation"].get("Date de la consultation", "")),
            ("motif", data["Informations sur la Consultation"].get("Motif de la consultation", "")),
            ("symptomes", data["Informations sur la Consultation"].get("Symptômes", "")),
            ("diagnostic", data["Informations sur la Consultation"].get("Diagnostic", "")),
            ("medecin", data["Informations sur la Consultation"].get("Médecin responsable", "")),
            ("temperature", data["Tests Médicaux"].get("Température corporelle", "")),
            ("tension", data["Tests Médicaux"].get("Tension artérielle", "")),
            ("imc", data["Tests Médicaux"].get("Poids et taille (IMC)", "")),
            ("analyses", data["Tests Médicaux"].get("Résultats d’analyses", "")),
            ("medicaments", data["Traitement & Prescription Médicale"].get("Médicaments prescrits", "")),
            ("conseils", data["Traitement & Prescription Médicale"].get("Conseils et recommandations médicales", "")),
            ("prochain_rdv", data["Traitement & Prescription Médicale"].get("Prochain rendez-vous", "")),
            ("consentement", data["Consentements & Signature"].get("Consentement du patient", "")),
            ("signature_medecin", data["Consentements & Signature"].get("Signature du médecin", "")),
            ("signature_patient", data["Consentements & Signature"].get("Signature du patient", "")),
            ("fichier", fichier)
        ]

        # Insérer chaque champ individuellement et vérifier l'insertion
        for champ, valeur in champs_valeurs:
            cursor.execute(f"UPDATE dossiers_medical SET {champ} = %s WHERE utilisateur_id = %s", (valeur, utilisateur_id))
            conn.commit()
            # Vérifier si la mise à jour a affecté au moins une ligne
            if cursor.rowcount > 0:
                print(f"Insertion réussie pour le champ '{champ}'.")
            else:
                print(f"Aucune modification effectuée pour le champ '{champ}'.")

        print("Tous les champs ont été traités.")
     except Exception as e:
        print("Une erreur est survenue lors de l'insertion :", e)


    window.title("Formulaire Médical")
    window.geometry("700x750")
    main_frame = LabelFrame(window, text="Formulaire Médical", font=("Arial", 14, "bold"), padx=10, pady=10, bd=2, relief="ridge", fg="blue")
    main_frame.pack(padx=20, pady=20, fill="both", expand=True)

    canvas = Canvas(main_frame)
    scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    sections = {
        "Antécédents Médicaux": [
            "Antécédents familiaux", "Antécédents personnels", "Interventions chirurgicales passées", 
            "Vaccinations", "Traitements en cours"
        ],
        "Informations sur la Consultation": [
            "Date de la consultation", "Motif de la consultation", "Symptômes", 
            "Diagnostic", "Médecin responsable"
        ],
        "Tests Médicaux": [
            "Température corporelle", "Tension artérielle", "Poids et taille (IMC)", "Résultats d’analyses"
        ],
        "Traitement & Prescription Médicale": [
            "Médicaments prescrits", "Conseils et recommandations médicales", "Prochain rendez-vous"
        ],
        "Consentements & Signature": [
            "Consentement du patient", "Signature du médecin", "Signature du patient"
        ]
    }

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
            entry.pack_forget()
            entries.append(entry)
            variables.append(var)
        sections[section] = {"elements": elements, "variables": variables, "entries": entries}

    fichier_frame = LabelFrame(scrollable_frame, text="Ajout de Fichier Médical", font=("Arial", 12, "bold"), padx=10, pady=10, bd=1, relief="solid")
    fichier_frame.pack(pady=20, padx=10, fill="x")
    ajouter_btn = Button(fichier_frame, text="Ajouter un fichier médical", command=ajouter_fichier, bg="blue", fg="white")
    ajouter_btn.pack(pady=5)
    fichier_label = Label(fichier_frame, text="", wraplength=500, fg="black")
    fichier_label.pack(pady=5)
    submit_btn = Button(scrollable_frame, text="Soumettre", command=submit, bg="green", fg="white")
    submit_btn.pack(pady=20)

    # Placer la gestion de la fermeture AVANT mainloop
    def fermer_connexion():
       cursor.close()
       conn.close()

    window.protocol("WM_DELETE_WINDOW", fermer_connexion)
    window.mainloop()


 


from tkinter import *
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
import mysql.connector
import re

##########################################################################
# Fonctions utilitaires et formulaire médical (Dossier Médical)
##########################################################################

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",         # Adaptez le user si nécessaire
        password="",         # Adaptez le password si nécessaire
        database="formulaire"
    )

def formulaire_medicale(window, utilisateur_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Création de la table dossiers_medical si elle n'existe pas
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

    def ajouter_fichier():
        fichier_path = filedialog.askopenfilename(
            title="Sélectionner un fichier médical",
            filetypes=[
                ("Tous les fichiers", "."),
                ("PDF", "*.pdf"),
                ("Images", ".jpg;.png"),
                ("Documents", ".docx;.txt")
            ]
        )
        if fichier_path:
            fichier_label.config(text=f"Fichier sélectionné: {fichier_path}")

    def afficher_entry(section, index):
        if sections[section]["variables"][index].get():
            sections[section]["entries"][index].pack(side="left", padx=5)
        else:
            sections[section]["entries"][index].pack_forget()

    def submit():
        try:
            # Récupération des valeurs saisies dans chaque section
            data = {section: {} for section in sections.keys()}
            for section, content in sections.items():
                for i, var in enumerate(content["variables"]):
                    if var.get():
                        data[section][content["elements"][i]] = content["entries"][i].get()
            # Récupération du chemin de fichier
            fichier = fichier_label.cget("text").replace("Fichier sélectionné: ", "")

            # Liste des champs et valeurs à mettre à jour  
            # (on n'inclut pas utilisateur_id dans UPDATE puisqu'il sert de clé)
            champs_valeurs = [
                ("antecedents_familiaux", data["Antécédents Médicaux"].get("Antécédents familiaux", "")),
                ("antecedents_personnels", data["Antécédents Médicaux"].get("Antécédents personnels", "")),
                ("interventions", data["Antécédents Médicaux"].get("Interventions chirurgicales passées", "")),
                ("vaccinations", data["Antécédents Médicaux"].get("Vaccinations", "")),
                ("traitements", data["Antécédents Médicaux"].get("Traitements en cours", "")),
                ("date_consultation", data["Informations sur la Consultation"].get("Date de la consultation", "")),
                ("motif", data["Informations sur la Consultation"].get("Motif de la consultation", "")),
                ("symptomes", data["Informations sur la Consultation"].get("Symptômes", "")),
                ("diagnostic", data["Informations sur la Consultation"].get("Diagnostic", "")),
                ("medecin", data["Informations sur la Consultation"].get("Médecin responsable", "")),
                ("temperature", data["Tests Médicaux"].get("Température corporelle", "")),
                ("tension", data["Tests Médicaux"].get("Tension artérielle", "")),
                ("imc", data["Tests Médicaux"].get("Poids et taille (IMC)", "")),
                ("analyses", data["Tests Médicaux"].get("Résultats d’analyses", "")),
                ("medicaments", data["Traitement & Prescription Médicale"].get("Médicaments prescrits", "")),
                ("conseils", data["Traitement & Prescription Médicale"].get("Conseils et recommandations médicales", "")),
                ("prochain_rdv", data["Traitement & Prescription Médicale"].get("Prochain rendez-vous", "")),
                ("consentement", data["Consentements & Signature"].get("Consentement du patient", "")),
                ("signature_medecin", data["Consentements & Signature"].get("Signature du médecin", "")),
                ("signature_patient", data["Consentements & Signature"].get("Signature du patient", "")),
                ("fichier", fichier)
            ]

            # Vérification de l'existence d'un dossier pour cet utilisateur
            cursor.execute("SELECT COUNT(*) FROM dossiers_medical WHERE utilisateur_id = %s", (utilisateur_id,))
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO dossiers_medical (utilisateur_id) VALUES (%s)", (utilisateur_id,))
                conn.commit()
                print(f"Nouvel enregistrement créé pour utilisateur_id = {utilisateur_id}")
            else:
                print(f"Enregistrement existant trouvé pour utilisateur_id = {utilisateur_id}")

            # Mise à jour de chaque champ
            for champ, valeur in champs_valeurs:
                cursor.execute(f"UPDATE dossiers_medical SET {champ} = %s WHERE utilisateur_id = %s", (valeur, utilisateur_id))
                conn.commit()
                if cursor.rowcount > 0:
                    print(f"Insertion réussie pour le champ '{champ}'.")
                else:
                    print(f"Aucune modification effectuée pour le champ '{champ}'.")
            print("Tous les champs ont été traités.")

        except Exception as e:
            print("Une erreur est survenue lors de l'insertion :", e)

    # Construction de l'interface du formulaire médical
    window.title("Formulaire Médical")
    window.geometry("700x750")

    main_frame = LabelFrame(window, text="Formulaire Médical", font=("Arial", 14, "bold"), padx=10, pady=10, bd=2, relief="ridge", fg="blue")
    main_frame.pack(padx=20, pady=20, fill="both", expand=True)

    canvas = Canvas(main_frame)
    scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Définition des sections et de leurs champs
    sections = {
        "Antécédents Médicaux": [
            "Antécédents familiaux", "Antécédents personnels", "Interventions chirurgicales passées", 
            "Vaccinations", "Traitements en cours"
        ],
        "Informations sur la Consultation": [
            "Date de la consultation", "Motif de la consultation", "Symptômes", 
            "Diagnostic", "Médecin responsable"
        ],
        "Tests Médicaux": [
            "Température corporelle", "Tension artérielle", "Poids et taille (IMC)", "Résultats d’analyses"
        ],
        "Traitement & Prescription Médicale": [
            "Médicaments prescrits", "Conseils et recommandations médicales", "Prochain rendez-vous"
        ],
        "Consentements & Signature": [
            "Consentement du patient", "Signature du médecin", "Signature du patient"
        ]
    }

    # Création dynamique des widgets pour chaque section
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
            entry.pack_forget()
            entries.append(entry)
            variables.append(var)
        sections[section] = {"elements": elements, "variables": variables, "entries": entries}

    # Zone pour l'ajout du fichier médical
    fichier_frame = LabelFrame(scrollable_frame, text="Ajout de Fichier Médical", font=("Arial", 12, "bold"), padx=10, pady=10, bd=1, relief="solid")
    fichier_frame.pack(pady=20, padx=10, fill="x")
    ajouter_btn = Button(fichier_frame, text="Ajouter un fichier médical", command=ajouter_fichier, bg="blue", fg="white")
    ajouter_btn.pack(pady=5)
    fichier_label = Label(fichier_frame, text="", wraplength=500, fg="black")
    fichier_label.pack(pady=5)
    submit_btn = Button(scrollable_frame, text="Soumettre", command=submit, bg="green", fg="white")
    submit_btn.pack(pady=20)

    def fermer_connexion():
        cursor.close()
        conn.close()

    window.protocol("WM_DELETE_WINDOW", fermer_connexion)
    window.mainloop()

##########################################################################
# Classe Formulaire : inscription de l'utilisateur et ouverture du
# formulaire médical une fois l'enregistrement terminé.
##########################################################################

class Formulaire:
    def __init__(self, root):
        self.root = root
        self.root.title("Formulaire")
        self.root.geometry("800x600")
        self.root.configure(bg="#F5F5F5")

        # Création de la base de données et de la table utilisateurs
        self.creer_base_et_table()

        # Cadre principal pour afficher le formulaire
        frame1 = Frame(root, bg="white", bd=2, relief=RIDGE)
        frame1.place(relx=0.5, rely=0.5, anchor=CENTER, width=500, height=550)

        # Titre
        Label(frame1, text="Formulaire", font=("Times New Roman", 20, "bold"), bg="white", fg="dark blue") \
            .grid(row=1, column=1, columnspan=4, pady=15)

        # Champs d'inscription
        Label(frame1, text="Prénom:", bg="white").grid(row=2, column=0, padx=20, pady=5, sticky=W)
        self.entry_prenom = ttk.Entry(frame1, width=30)
        self.entry_prenom.grid(row=2, column=1, pady=5)

        Label(frame1, text="Nom:", bg="white").grid(row=4, column=0, padx=20, pady=5, sticky=W)
        self.entry_nom = ttk.Entry(frame1, width=30)
        self.entry_nom.grid(row=4, column=1, pady=5)

        Label(frame1, text="Date de naissance:", bg="white").grid(row=6, column=0, padx=20, pady=5, sticky=W)
        self.date_entry = DateEntry(frame1, width=20, font=("Times New Roman", 12), date_pattern="yyyy-MM-dd")
        self.date_entry.grid(row=6, column=1, pady=5)

        Label(frame1, text="Sexe:", bg="white").grid(row=8, column=0, padx=20, pady=5, sticky=W)
        self.gender = StringVar()
        frame_gender = Frame(frame1, bg="white")
        frame_gender.grid(row=8, column=1, pady=5)
        ttk.Radiobutton(frame_gender, text="Masculin", variable=self.gender, value="Masculin") \
            .pack(side=LEFT, padx=10)
        ttk.Radiobutton(frame_gender, text="Féminin", variable=self.gender, value="Féminin") \
            .pack(side=LEFT, padx=10)

        Label(frame1, text="Numéro de téléphone:", bg="white").grid(row=10, column=0, padx=20, pady=5, sticky=W)
        self.entry_numeroTel = ttk.Entry(frame1, width=30)
        self.entry_numeroTel.grid(row=10, column=1, pady=5)

        Label(frame1, text="Email:", bg="white").grid(row=12, column=0, padx=20, pady=5, sticky=W)
        self.entry_email = ttk.Entry(frame1, width=30)
        self.entry_email.grid(row=12, column=1, pady=5)
        self.entry_email.bind("<KeyRelease>", self.verifier_email)

        # Bouton d'enregistrement
        Button(frame1, text="Enregistrer", font=("Times New Roman", 15), bg="dark blue", fg="white", 
               command=self.enregistrer_donnees).grid(row=14, column=1, pady=20)
    
    def creer_base_et_table(self):
        """ Crée la base de données et la table utilisateurs si elles n'existent pas """
        try:
            con = mysql.connector.connect(host='localhost', user='root', password='')
            mycur = con.cursor()
            mycur.execute("CREATE DATABASE IF NOT EXISTS formulaire")
            con.commit()
            con.close()

            con = mysql.connector.connect(host='localhost', user='root', password='', database='formulaire')
            mycur = con.cursor()
            mycur.execute("""
                CREATE TABLE IF NOT EXISTS utilisateurs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    prenom VARCHAR(50),
                    nom VARCHAR(50),
                    date_naissance DATE,
                    sexe ENUM('Masculin', 'Féminin'),
                    numero_tel VARCHAR(20),
                    email VARCHAR(100) UNIQUE
                )
            """)
            con.commit()
            con.close()
        except mysql.connector.Error as e:
            print(f"Erreur MySQL : {e}")

    def verifier_email(self, event):
        """ Vérifie si l'email saisi est valide et change la couleur du texte """
        email = self.entry_email.get()
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        self.entry_email.config(foreground="black" if re.match(pattern, email) else "red")

    def enregistrer_donnees(self):
        """ Enregistre les données de l'utilisateur et ouvre le formulaire médical """
        prenom = self.entry_prenom.get()
        nom = self.entry_nom.get()
        date_naissance = self.date_entry.get()
        sexe = self.gender.get()
        numero_tel = self.entry_numeroTel.get()
        email = self.entry_email.get()

        if not all([prenom, nom, date_naissance, sexe, numero_tel, email]):
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis !", parent=self.root)
            return

        if not re.match(r"^\d{10}$", numero_tel):
            messagebox.showerror("Erreur", "Numéro de téléphone invalide !", parent=self.root)
            return

        try:
            con = mysql.connector.connect(host='localhost', user='root', password='', database='formulaire')
            mycur = con.cursor()
            # Vérifier si l'email est déjà utilisé
            mycur.execute("SELECT * FROM utilisateurs WHERE email = %s", (email,))
            if mycur.fetchone():
                messagebox.showerror("Erreur", "Cet email est déjà utilisé !", parent=self.root)
                return

            mycur.execute("INSERT INTO utilisateurs (prenom, nom, date_naissance, sexe, numero_tel, email) VALUES (%s, %s, %s, %s, %s, %s)",
                          (prenom, nom, date_naissance, sexe, numero_tel, email))
            con.commit()

            # Récupération de l'id de l'utilisateur inscrit
            mycur.execute("SELECT id FROM utilisateurs WHERE email = %s", (email,))
            utilisateur_id = mycur.fetchone()[0]
            con.close()

            # Fermer la fenêtre d'inscription et ouvrir le formulaire médical
            self.root.destroy()
            dossier_window = Toplevel()
            formulaire_medicale(dossier_window, utilisateur_id)

            messagebox.showinfo("Succès", "Ajout effectué !", parent=self.root)

        except mysql.connector.Error as e:
            messagebox.showerror("Erreur", f"Erreur de connexion : {e}", parent=self.root)

##########################################################################
# Programme principal
##########################################################################

if __name__ == "__main__":
    root = Tk()
    app = Formulaire(root)
    root.mainloop()
