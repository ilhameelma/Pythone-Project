from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector
import re
from tkinter import filedialog, messagebox
from tkinter import Tk, Button, Label, Entry, Frame, Canvas, Scrollbar, BOTH, LEFT, RIGHT, Y, VERTICAL
from tkinter import ttk, messagebox

# Fonction de connexion à MySQL

 


from tkinter import *
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
import mysql.connector
import re

##########################################################################
# Fonctions utilitaires et formulaire médical (Dossier Médical)
##########################################################################
def ajouter_patien():
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
            abelVide=Label(frame1, text="",bg="white").grid(row=3, column=0, padx=20)  # Espacement vertical


            Label(frame1, text="Nom:", bg="white").grid(row=4, column=0, padx=20, pady=5, sticky=W)
            self.entry_nom = ttk.Entry(frame1, width=30)
            self.entry_nom.grid(row=4, column=1, pady=5)
            abelVide=Label(frame1, text="",bg="white").grid(row=5, column=0, padx=20)  # Espacement vertical


            Label(frame1, text="Date de naissance:", bg="white").grid(row=6, column=0, padx=20, pady=5, sticky=W)
            self.date_entry = DateEntry(frame1, width=20, font=("Times New Roman", 12), date_pattern="yyyy-MM-dd")
            self.date_entry.grid(row=6, column=1, pady=5)
            abelVide=Label(frame1, text="",bg="white").grid(row=7, column=0, padx=20)  # Espacement vertical

            Label(frame1, text="Sexe:", bg="white").grid(row=8, column=0, padx=20, pady=5, sticky=W)
            self.gender = StringVar()
            frame_gender = Frame(frame1, bg="white")
            frame_gender.grid(row=8, column=1, pady=5)
            ttk.Radiobutton(frame_gender, text="Masculin", variable=self.gender, value="Masculin") \
                .pack(side=LEFT, padx=10)
            ttk.Radiobutton(frame_gender, text="Féminin", variable=self.gender, value="Féminin") \
                .pack(side=LEFT, padx=10)
            

            abelVide=Label(frame1, text="",bg="white").grid(row=9, column=0, padx=20)  # Espacement vertical
            Label(frame1, text="Numéro de téléphone:", bg="white").grid(row=10, column=0, padx=20, pady=5, sticky=W)
            self.entry_numeroTel = ttk.Entry(frame1, width=30)
            self.entry_numeroTel.grid(row=10, column=1, pady=5)
            

            abelVide=Label(frame1, text="",bg="white").grid(row=11, column=0, padx=20)  # Espacement vertical
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
            """
            if not all([prenom, nom, date_naissance, sexe, numero_tel, email]):
                messagebox.showerror("Erreur", "Tous les champs doivent être remplis !", parent=self.root)
                return"""

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
        
        
from tkinter import *
from tkinter import messagebox, ttk

def supprimer_container():
    window = Tk()
    window.title("Suppression Utilisateur")
    window.geometry("400x250")  # Taille ajustée
    window.resizable(False, False)  # Empêcher le redimensionnement

    # Fonction pour changer le style du bouton au survol
    def on_hover(event):
        btn_supprimer.configure(style="Hover.TButton")

    def on_leave(event):
        btn_supprimer.configure(style="Red.TButton")

    # Style des composants
    style = ttk.Style()
    style.configure("Red.TButton", background="#DC3545", foreground="white", font=("Arial", 12, "bold"))
    style.map("Red.TButton", background=[("active", "#A71D2A")])
    style.configure("Hover.TButton", background="#A71D2A", foreground="white", font=("Arial", 12, "bold"))

    # Label stylisé
    label_supprimer = Label(window, text="Donner l'ID de l'utilisateur à supprimer :", fg="#007BFF", font=("Arial", 10, "bold"))
    label_supprimer.pack(pady=10)

    # Champ de saisie
    entry_supprimer = Entry(window, font=("Arial", 12))
    entry_supprimer.pack(pady=5)

    # Fonction pour la connexion à la base de données
    def get_connection():
        import mysql.connector
        return mysql.connector.connect(
            host="localhost",
            user="root",  
            password="",  
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

            # Suppression
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

    # Bouton stylisé avec hover
    btn_supprimer = ttk.Button(window, text="Supprimer", style="Red.TButton", command=supprimer_utilisateur)
    btn_supprimer.pack(pady=20)

    btn_supprimer.bind("<Enter>", on_hover)
    btn_supprimer.bind("<Leave>", on_leave)

    # Lancer l'application
    window.mainloop()



    
def modifier_container():
    # Fonction pour établir la connexion MySQL
    def get_connection():
        return mysql.connector.connect(
            host="localhost",
            user="root",  
            password="",  
            database="formulaire"
        )

    # Fonction pour récupérer les anciennes valeurs de l'utilisateur
    def get_old_values(user_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM utilisateurs WHERE id = %s", (user_id,))
        user_data = cursor.fetchone()
        
        cursor.execute("SELECT * FROM dossiers_medical WHERE utilisateur_id = %s", (user_id,))
        medical_data = cursor.fetchone()
        
        conn.close()
        
        return user_data, medical_data

    # Fonction pour modifier un utilisateur
    def modifier_utilisateur():
        user_id = entry_modifier.get().strip()

        if not user_id.isdigit():
            messagebox.showerror("Erreur", "L'ID doit être un nombre valide.")
            return

        try:
            # Récupération des anciennes valeurs
            old_user, old_medical = get_old_values(user_id)

            if not old_user:
                messagebox.showerror("Erreur", "Utilisateur non trouvé.")
                return
            
            # Récupération des nouvelles valeurs (si vide, on garde l'ancienne)
            new_values = {
                "email": entry_email.get().strip() or old_user["email"],
                "numero_tel": entry_numtel.get().strip() or old_user["numero_tel"],
                "antecedents_familiaux": entry_Antécédents_familiaux.get().strip() or old_medical["antecedents_familiaux"],
                "antecedents_personnels": entry_Antécédents_personnels.get().strip() or old_medical["antecedents_personnels"],
                "interventions": entry_Interventions_chirurgicales.get().strip() or old_medical["interventions"],
                "vaccinations": entry_Vaccinations.get().strip() or old_medical["vaccinations"],
                "traitements": entry_Traitements_cours.get().strip() or old_medical["traitements"],
                "date_consultation": entry_Date_consultation.get().strip() or old_medical["date_consultation"],
                "motif": entry_Motif_consultation.get().strip() or old_medical["motif"],
                "symptomes": entry_Symptômes.get().strip() or old_medical["symptomes"],
                "diagnostic": entry_Diagnostic.get().strip() or old_medical["diagnostic"],
                "temperature": entry_Température_corporelle.get().strip() or old_medical["temperature"],
                "tension": entry_tention.get().strip() or old_medical["tension"],
                "medicaments": entry_Médicaments_prescrits.get().strip() or old_medical["medicaments"],
                "conseils": entry_Conseils_recommandations.get().strip() or old_medical["conseils"],
                "prochain_rdv": entry_Prochain_rendezvous.get().strip() or old_medical["prochain_rdv"]
            }

            # Connexion et mise à jour
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE utilisateurs SET email=%s, numero_tel=%s WHERE id=%s",
                (new_values["email"], new_values["numero_tel"], user_id)
            )

            cursor.execute(
                """
                UPDATE dossiers_medical SET
                    antecedents_familiaux=%s, antecedents_personnels=%s, interventions=%s,
                    vaccinations=%s, traitements=%s, date_consultation=%s, motif=%s, symptomes=%s,
                    diagnostic=%s, temperature=%s, tension=%s, conseils=%s, prochain_rdv=%s, medicaments=%s
                WHERE utilisateur_id=%s
                """,
                (new_values["antecedents_familiaux"], new_values["antecedents_personnels"],
                new_values["interventions"], new_values["vaccinations"], new_values["traitements"],
                new_values["date_consultation"], new_values["motif"], new_values["symptomes"],
                new_values["diagnostic"], new_values["temperature"], new_values["tension"],
                new_values["conseils"], new_values["prochain_rdv"], new_values["medicaments"], user_id)
            )

            conn.commit()
            messagebox.showinfo("Succès", "Informations mises à jour avec succès.")

        except mysql.connector.Error as e:
            messagebox.showerror("Erreur", f"Erreur MySQL : {e}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    # Création de la fenêtre principale
    window = Tk()
    window.title("Modifier Utilisateur")
    window.geometry("600x600")  # Taille ajustée
    window.configure(bg="#f0f0f0")
    # Création d'un Canvas pour permettre le défilement
    main_frame = Frame(window)
    main_frame.pack(fill=BOTH, expand=1)

    canvas = Canvas(main_frame, bg="#f0f0f0")
    canvas.pack(side=LEFT, fill=BOTH, expand=1)

    scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Frame pour contenir le formulaire
    form_frame = Frame(canvas, bg="#f0f0f0")
    canvas.create_window((0, 0), window=form_frame, anchor="nw")
    def create_label(text):
        return Label(form_frame, text=text, fg="#007BFF", font=("Arial", 10, "bold"))
    # Style
    style = ttk.Style()
    style.configure("TLabel", font=("Arial", 12), background="#f0f0f0",fg="blue")
    style.configure("TButton", font=("Arial", 12), padding=5)
    style.configure("TEntry", padding=5)
    # Ajouter les champs du formulaire
    create_label("ID de l'utilisateur à modifier :").pack()
    entry_modifier = ttk.Entry(form_frame)
    entry_modifier.pack(pady=5)

    create_label("Nouvel Email :").pack(pady=5)
    entry_email =ttk.Entry(form_frame)
    entry_email.pack(pady=5)

    create_label("Nouveau numéro de téléphone :").pack(pady=5)
    entry_numtel = ttk.Entry(form_frame)
    entry_numtel.pack(pady=5)

    create_label("Antécédents familiaux :").pack(pady=5)
    entry_Antécédents_familiaux = ttk.Entry(form_frame)
    entry_Antécédents_familiaux.pack(pady=5)

    create_label("Antécédents personnels :").pack(pady=5)
    entry_Antécédents_personnels = ttk.Entry(form_frame)
    entry_Antécédents_personnels.pack(pady=5)

    create_label("Interventions chirurgicales :").pack(pady=5)
    entry_Interventions_chirurgicales = ttk.Entry(form_frame)
    entry_Interventions_chirurgicales.pack(pady=5)

    create_label("Vaccinations :").pack(pady=5)
    entry_Vaccinations = ttk.Entry(form_frame)
    entry_Vaccinations.pack(pady=5)

    create_label("Traitements en cours :").pack(pady=5)
    entry_Traitements_cours = ttk.Entry(form_frame)
    entry_Traitements_cours.pack(pady=5)

    create_label("Date de consultation :").pack(pady=5)
    entry_Date_consultation = ttk.Entry(form_frame)
    entry_Date_consultation.pack(pady=5)

    create_label("Motif de la consultation :").pack(pady=5)
    entry_Motif_consultation = ttk.Entry(form_frame)
    entry_Motif_consultation.pack(pady=5)

    create_label("Symptômes :").pack(pady=5)
    entry_Symptômes = ttk.Entry(form_frame)
    entry_Symptômes.pack(pady=5)

    create_label("Diagnostic :").pack(pady=5)
    entry_Diagnostic = ttk.Entry(form_frame)
    entry_Diagnostic.pack(pady=5)

    create_label("Température corporelle :").pack(pady=5)
    entry_Température_corporelle = ttk.Entry(form_frame)
    entry_Température_corporelle.pack(pady=5)

    create_label("Tension :").pack(pady=5)
    entry_tention = ttk.Entry(form_frame)
    entry_tention.pack(pady=5)

    create_label("Médicaments prescrits :").pack(pady=5)
    entry_Médicaments_prescrits = ttk.Entry(form_frame)
    entry_Médicaments_prescrits.pack(pady=5)

    create_label("Conseils médicaux :").pack(pady=5)
    entry_Conseils_recommandations = ttk.Entry(form_frame)
    entry_Conseils_recommandations.pack(pady=5)

    create_label("Prochain rendez-vous :").pack(pady=5)
    entry_Prochain_rendezvous = ttk.Entry(form_frame)
    entry_Prochain_rendezvous.pack(pady=5)

    # Bouton pour modifier les informations
    btn_modifier = ttk.Button(form_frame, text="Modifier les informations", command=modifier_utilisateur)
    btn_modifier.pack(pady=10)

    window.mainloop()

  

import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime
import mysql.connector
from tkinter import Frame, Label, RIDGE, CENTER, LEFT, StringVar

def guerison():
    def get_connection():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="formulaire"
        )

    def formulaire_guerison(utilisateur_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nom, prenom FROM utilisateurs WHERE id = %s", (utilisateur_id,))
        utilisateur = cursor.fetchone()
        nom = utilisateur[0] if utilisateur else "Inconnu"
        prenom = utilisateur[1] if utilisateur else "Inconnu"

        cursor.execute('''CREATE TABLE IF NOT EXISTS guerison (
            id INT AUTO_INCREMENT PRIMARY KEY,
            utilisateur_id INT,
            date_debut_traitement DATE,
            date_fin_guerison DATE,
            etat_sante_actuel TEXT,
            symptomes_persistants TEXT,
            traitement_en_cours TEXT,
            etat_guerison ENUM('Guéri', 'En Cours', 'Non Guéri') NOT NULL,
            FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id)
        )''')
        conn.commit()

        def save_data():
            date_debut_traitement = entry_date_debut.get()
            date_fin_guerison = entry_date_fin.get()
            etat_sante_actuel = entry_etat_sante.get()
            symptomes_persistants = entry_symptomes.get()
            traitement_en_cours = entry_traitement.get()
            etat_guerison = etat_guerison_var.get()

            if not etat_guerison:
                messagebox.showerror("Erreur", "Le champ 'État final de guérison' doit être rempli !")
                return
            try:
                date_debut = datetime.strptime(date_debut_traitement, "%Y-%m-%d")
                date_fin = datetime.strptime(date_fin_guerison, "%Y-%m-%d") if date_fin_guerison else None
                if date_fin and date_fin <= date_debut:
                    messagebox.showerror("Erreur", "La date de fin doit être postérieure à la date de début.")
                    return
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer des dates valides !")
                return

            cursor.execute("SELECT * FROM guerison WHERE utilisateur_id = %s", (utilisateur_id,))
            if cursor.fetchone():
                cursor.execute('''UPDATE guerison
                    SET date_debut_traitement = %s, date_fin_guerison = %s, etat_sante_actuel = %s,
                    symptomes_persistants = %s, traitement_en_cours = %s, etat_guerison = %s
                    WHERE utilisateur_id = %s''',
                               (date_debut_traitement, date_fin_guerison, etat_sante_actuel,
                                symptomes_persistants, traitement_en_cours, etat_guerison, utilisateur_id))
            else:
                cursor.execute('''INSERT INTO guerison (
                    utilisateur_id, date_debut_traitement, date_fin_guerison, etat_sante_actuel,
                    symptomes_persistants, traitement_en_cours, etat_guerison
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                               (utilisateur_id, date_debut_traitement, date_fin_guerison, etat_sante_actuel,
                                symptomes_persistants, traitement_en_cours, etat_guerison))
            conn.commit()
            conn.close()

            messagebox.showinfo("Succès", "Les informations de guérison ont été enregistrées avec succès.")
            window.destroy()

        # Interface stylée
        window = tk.Tk()
        window.title("Formulaire de Guérison")
        window.geometry("800x600")
        window.configure(bg="#F5F5F5")

        frame = Frame(window, bg="white", bd=2, relief=RIDGE)
        frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=550, height=550)

        Label(frame, text="Formulaire de Guérison", font=("Times New Roman", 20, "bold"), bg="white", fg="dark blue").grid(row=0, column=0, columnspan=2, pady=20)

        Label(frame, text="Nom:", bg="white").grid(row=1, column=0, padx=20, pady=5, sticky="w")
        entry_nom = ttk.Entry(frame, width=30)
        entry_nom.insert(0, nom)
        entry_nom.config(state="readonly")
        entry_nom.grid(row=1, column=1, pady=5)
          
        abelVide=Label(frame, text="",bg="white").grid(row=2, column=0, padx=20)  # Espacement vertical
        Label(frame, text="Prénom:", bg="white").grid(row=3, column=0, padx=20, pady=5, sticky="w")
        entry_prenom = ttk.Entry(frame, width=30)
        entry_prenom.insert(0, prenom)
        entry_prenom.config(state="readonly")
        entry_prenom.grid(row=3, column=1, pady=5)
        abelVide=Label(frame, text="",bg="white").grid(row=4, column=0, padx=20)  # Espacement vertical
        Label(frame, text="Date début traitement:", bg="white").grid(row=5, column=0, padx=20, pady=5, sticky="w")
        entry_date_debut = DateEntry(frame, width=20, font=("Times New Roman", 12), date_pattern="yyyy-MM-dd")
        entry_date_debut.grid(row=5, column=1, pady=5)
        abelVide=Label(frame, text="",bg="white").grid(row=6, column=0, padx=20)  # Espacement vertical
        Label(frame, text="Date fin guérison:", bg="white").grid(row=7, column=0, padx=20, pady=5, sticky="w")
        entry_date_fin = DateEntry(frame, width=20, font=("Times New Roman", 12), date_pattern="yyyy-MM-dd")
        entry_date_fin.grid(row=7, column=1, pady=5)
        abelVide=Label(frame, text="",bg="white").grid(row=8, column=0, padx=20)  # Espacement vertical
        Label(frame, text="État de santé actuel:", bg="white").grid(row=9, column=0, padx=20, pady=5, sticky="w")
        entry_etat_sante = ttk.Entry(frame, width=30)
        entry_etat_sante.grid(row=9, column=1, pady=5)
        abelVide=Label(frame, text="",bg="white").grid(row=10, column=0, padx=20)  # Espacement vertical
        Label(frame, text="Symptômes persistants:", bg="white").grid(row=11, column=0, padx=20, pady=5, sticky="w")
        entry_symptomes = ttk.Entry(frame, width=30)
        entry_symptomes.grid(row=11, column=1, pady=5)
        abelVide=Label(frame, text="",bg="white").grid(row=12, column=0, padx=20)  # Espacement vertical
        Label(frame, text="Traitement en cours:", bg="white").grid(row=13, column=0, padx=20, pady=5, sticky="w")
        entry_traitement = ttk.Entry(frame, width=30)
        entry_traitement.grid(row=13, column=1, pady=5)
        abelVide=Label(frame, text="",bg="white").grid(row=14, column=0, padx=20)  # Espacement vertical
        Label(frame, text="État final de guérison:", bg="white").grid(row=15, column=0, padx=20, pady=5, sticky="w")
        etat_guerison_var = StringVar(value="En Cours")
        frame_radio = Frame(frame, bg="white")
        frame_radio.grid(row=15, column=1, pady=5, sticky="w")
        ttk.Radiobutton(frame_radio, text="Guéri", variable=etat_guerison_var, value="Guéri").pack(side=LEFT, padx=5)
        ttk.Radiobutton(frame_radio, text="En Cours", variable=etat_guerison_var, value="En Cours").pack(side=LEFT, padx=5)
        ttk.Radiobutton(frame_radio, text="Non Guéri", variable=etat_guerison_var, value="Non Guéri").pack(side=LEFT, padx=5)

        tk.Button(frame, text="Enregistrer", font=("Times New Roman", 15), bg="dark blue", fg="white",
                  command=save_data).grid(row=16, column=1, columnspan=2, pady=20)

        window.mainloop()

    # Fenêtre ID utilisateur
    main_window = tk.Tk()
    main_window.title("Vérification ID utilisateur")
    main_window.geometry("500x200")
    main_window.config(bg="#F5F5F5")

    frame_id = Frame(main_window, bg="white", bd=2, relief=RIDGE)
    frame_id.place(relx=0.5, rely=0.5, anchor=CENTER, width=400, height=150)

    Label(frame_id, text="Entrez votre ID utilisateur:", font=("Arial", 12), bg="white").grid(row=0, column=0, padx=10, pady=20)
    entry_id_utilisateur = ttk.Entry(frame_id, width=30)
    entry_id_utilisateur.grid(row=0, column=1, padx=10, pady=20)

    def verifier_id():
        utilisateur_id = entry_id_utilisateur.get()
        if not utilisateur_id.isdigit():
            messagebox.showerror("Erreur", "L'ID utilisateur doit être un nombre.")
            return

        utilisateur_id = int(utilisateur_id)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM utilisateurs WHERE id = %s", (utilisateur_id,))
        if cursor.fetchone():
            main_window.destroy()
            formulaire_guerison(utilisateur_id)
        else:
            messagebox.showerror("Erreur", "ID utilisateur incorrect.")

    tk.Button(frame_id, text="Vérifier", bg="blue", fg="white", font=("Arial", 12, "bold"),
              command=verifier_id).grid(row=1, column=0, columnspan=2, pady=10)

    main_window.mainloop()















from tkinter import Tk, Label, Canvas, Toplevel
from tkinter import ttk
from PIL import Image, ImageTk  # Pour gérer les images

def menu_personnes_inscrites():
    # Création de la fenêtre secondaire avec Toplevel pour éviter les conflits avec Tk()
    window = Toplevel()
    window.title("Menu Utilisateur")
    window.geometry("800x700")
    window.resizable(False, False)  # Empêcher le redimensionnement

    # Charger et ajuster l'image de fond
    image_fond = Image.open("C:\\Users\\hp\\Downloads\\medical.png")
    image_fond = image_fond.resize((800, 700), Image.LANCZOS)
    bg_image = ImageTk.PhotoImage(image_fond)

    # Canvas pour afficher l'image sur toute la fenêtre
    canvas = Canvas(window, width=800, height=700)
    canvas.place(x=0, y=0)
    canvas.create_image(0, 0, anchor="nw", image=bg_image)  # Fond total

    # Stocker l'image pour éviter sa suppression
    window.bg_image = bg_image  

    # Création du titre
    label_titre = Label(window, text="Bienvenue", font=("Times New Roman", 24, "bold"), fg="white", bg="black")
    label_titre.place(relx=0.5, rely=0.2, anchor="center")

    # Boutons centrés
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 14, "bold"), padding=10, background="white")

    btn_modifier = ttk.Button(window, text="Modifier vos informations", style="TButton", command=modifier_container)
    btn_modifier.place(relx=0.5, rely=0.4, anchor="center", width=500)

    btn_guerison = ttk.Button(window, text="Remplir le formulaire de guérison", style="TButton", command=guerison)
    btn_guerison.place(relx=0.5, rely=0.5, anchor="center", width=500)

def main_menu():
    root = Tk()
    root.title("Menu Principal")
    root.geometry("400x300")

    Label(root, text="Menu Principal", font=("Arial", 16, "bold"), fg="blue").pack(pady=20)

    ttk.Button(root, text="Personnes déjà inscrites", command=menu_personnes_inscrites).pack(pady=10, fill="x")
    ttk.Button(root, text="Nouvelle Inscription", command=ajouter_patien).pack(pady=10, fill="x")

    root.mainloop()

# Programme principal
if __name__ == "__main__":
    main_menu()


