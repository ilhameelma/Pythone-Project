from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector
import re
from tkinter import filedialog, messagebox
from tkinter import Tk, Button, Label, Entry, Frame, Canvas, Scrollbar, BOTH, LEFT, RIGHT, Y, VERTICAL
from tkinter import ttk, messagebox
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import filedialog
import os
# Fonction pour envoyer l'email de confirmation avec un format HTML et un nom d'expéditeur professionnel
def envoyer_email_confirmation(email, user_id):
    try:
        # Configuration SMTP (à adapter avec vos informations)
        smtp_server = "smtp.gmail.com"  # Serveur SMTP (ex: Gmail)
        port = 587  # Port pour TLS
        expediteur = "elyaagoubi.samira2004@gmail.com"  # Votre adresse email
        motdepasse = "hdxziiibavovqily"  # Mot de passe ou mot de passe d'application
        
        # Construction du message HTML
        message = MIMEMultipart("alternative")
        message["Subject"] = "Confirmation d'inscription"
        message["From"] = "Service Médical <elyaagoubi.samira2004@gmail.com>"
        message["To"] = email
        
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <h2>Confirmation d'inscription</h2>
                <p>Bonjour,</p>
                <p>Merci pour votre inscription à notre service médical.</p>
                <p><strong>Identifiant patient (CI) :</strong> {user_id}<br>
                <strong>Email :</strong> {email}</p>
                <p>Conservez précieusement ces informations.</p>
                <br>
                <p>Cordialement,<br>L'équipe médicale</p>
                <p><small>Ce message a été envoyé automatiquement. Veuillez ne pas répondre à cet email.</small></p>
            </body>
        </html>
        """
        
        # Attachement HTML
        message.attach(MIMEText(html, "html"))
        
        # Connexion sécurisée au serveur SMTP
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()  # Chiffrement TLS
            server.login(expediteur, motdepasse)
            server.sendmail(expediteur, email, message.as_string())

        print(f"Email de confirmation envoyé à {email}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")
        # Vous pourriez logger cette erreur plutôt que de l'afficher

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
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS dossiers_medical (
            id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            utilisateur_id BIGINT UNSIGNED,
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
        ) AUTO_INCREMENT = 10000000
        ''')

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
                        id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                        prenom VARCHAR(50),
                        nom VARCHAR(50),
                        date_naissance DATE,
                        sexe ENUM('Masculin', 'Féminin'),
                        numero_tel VARCHAR(20),
                        email VARCHAR(100) UNIQUE
                    ) AUTO_INCREMENT = 10000000
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
                # ENVOI DE L'EMAIL DE CONFIRMATION
                envoyer_email_confirmation(email, utilisateur_id)
                con.close()

                # Fermer la fenêtre d'inscription et ouvrir le formulaire médical
                
                dossier_window = Toplevel()
                # Affichage du message de succès avec l'ID
                messagebox.showinfo(
                "Succès", 
                f"Inscription réussie !\nVotre ID utilisateur est : {utilisateur_id}\n"
                f"Un email de confirmation a été envoyé à {email}",
                parent=self.root
                 )
                self.root.destroy()
                formulaire_medicale(dossier_window, utilisateur_id)
            
                

                messagebox.showinfo("Succès", "Ajout effectué !", parent=self.root)
                if not self.root.winfo_ismapped():  # Vérifie si la fenêtre est cachée
                    self.root.deiconify()  # La rendre visible

    # Afficher le message avec le parent étant la fenêtre principale
                messagebox.showinfo("Succès", f"Ajout effectué pour CI code d'identification de l'utilisateur: = {utilisateur_id}", parent=self.root)
                

            except mysql.connector.Error as e:
                messagebox.showerror("Erreur", f"Erreur de connexion : {e}", parent=self.root)

    ##########################################################################
    # Programme principal
    ##########################################################################

    if __name__ == "__main__":
        from tkinter import messagebox
        root = Tk()
        app = Formulaire(root)
        utilisateur_id = cursor.lastrowid

        if self.root.winfo_exists():
            messagebox.showinfo("Succès", f"Ajout effectué pour CI code d'identification de l'utilisateur: = {utilisateur_id}", parent=self.root)

        root.mainloop()
        
# Fonction pour la connexion à la base de données
def supprimer_container():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="", 
        database="formulaire"
    )
    cursor = conn.cursor()

    root = Tk()
    root.title("Liste des Utilisateurs")
    root.geometry("1000x500")
    root.configure(bg="white")

    Label(root, text="Liste des Utilisateurs", font=("Arial", 18, "bold"), bg="white", fg="blue").pack(pady=10)

    colonnes = ("id", "prenom", "nom", "date_naissance", "sexe", "numero_tel", "email")
    tree = ttk.Treeview(root, columns=colonnes, show="headings")

    # Appliquer des couleurs avec style
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#ADD8E6", foreground="blue")
    style.map("Treeview", background=[("selected", "#3399FF")])

    # Définir les en-têtes
    for col in colonnes:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=130, anchor="center")

    # Appliquer des tags pour changer la couleur des lignes
    tree.tag_configure('oddrow', background="white")
    tree.tag_configure('evenrow', background="#f0f0f0")

    # Exécuter la requête
    cursor.execute("SELECT id, prenom, nom, date_naissance, sexe, numero_tel, email FROM utilisateurs")
    utilisateurs = cursor.fetchall()

    # Remplir le tableau avec des lignes colorées
    for index, utilisateur in enumerate(utilisateurs):
        tag = 'evenrow' if index % 2 == 0 else 'oddrow'
        tree.insert("", END, values=utilisateur, tags=(tag,))

    # Scrollbar
    scrollbar = Scrollbar(root, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    tree.pack(expand=True, fill=BOTH, padx=20, pady=10)

    # Fonction pour supprimer un utilisateur
    def supprimer_utilisateur():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner un utilisateur.")
            return

        user_id = tree.item(selected_item, "values")[0]  # On récupère l'ID de l'utilisateur sélectionné

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",  
                password="",  
                database="formulaire"
            )
            cursor = conn.cursor()

            # Suppression des données dans les tables
            cursor.execute("DELETE FROM dossiers_medical WHERE utilisateur_id = %s", (user_id,))
            cursor.execute("DELETE FROM utilisateurs WHERE id = %s", (user_id,))

            conn.commit()
            messagebox.showinfo("Succès", "Utilisateur supprimé avec succès.")
            # Réactualiser la liste des utilisateurs après suppression
            tree.delete(selected_item)

        except mysql.connector.Error as e:
            messagebox.showerror("Erreur", f"Erreur MySQL : {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    # Bouton de suppression
    btn_supprimer = Button(root, text="Supprimer Utilisateur", command=supprimer_utilisateur, font=("Arial", 12, "bold"), bg="#DC3545", fg="white")
    btn_supprimer.pack(pady=20)

    cursor.close()
    conn.close()
    root.mainloop()






    
def modifier_container(user_id):
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
def modifier():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="", 
        database="formulaire"
    )
    cursor = conn.cursor()

    root = Tk()
    root.title("Liste des Utilisateurs")
    root.geometry("1000x500")
    root.configure(bg="white")

    Label(root, text="Liste des Utilisateurs", font=("Arial", 18, "bold"), bg="white", fg="blue").pack(pady=10)

    colonnes = ("id", "prenom", "nom", "date_naissance", "sexe", "numero_tel", "email")
    tree = ttk.Treeview(root, columns=colonnes, show="headings")

    # Appliquer des couleurs avec style
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#ADD8E6", foreground="blue")
    style.map("Treeview", background=[("selected", "#3399FF")])

    # Définir les en-têtes
    for col in colonnes:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=130, anchor="center")

    # Appliquer des tags pour changer la couleur des lignes
    tree.tag_configure('oddrow', background="white")
    tree.tag_configure('evenrow', background="#f0f0f0")

    # Exécuter la requête
    cursor.execute("SELECT id, prenom, nom, date_naissance, sexe, numero_tel, email FROM utilisateurs")
    utilisateurs = cursor.fetchall()

    # Remplir le tableau avec des lignes colorées
    for index, utilisateur in enumerate(utilisateurs):
        tag = 'evenrow' if index % 2 == 0 else 'oddrow'
        tree.insert("", END, values=utilisateur, tags=(tag,))

    # Scrollbar
    scrollbar = Scrollbar(root, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    tree.pack(expand=True, fill=BOTH, padx=20, pady=10)
        # Ajouter un bouton pour modifier un utilisateur
    def ouvrir_modification():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Attention", "Veuillez sélectionner un utilisateur.")
            return

        selected_user = tree.item(selected_item)["values"]
        user_id = selected_user[0]  # C'est l'ID de l'utilisateur sélectionné

        root.destroy()
        modifier_container(user_id)



    bouton_modifier = Button(root, text="Modifier un Utilisateur", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=ouvrir_modification)
    bouton_modifier.pack(pady=10)


    cursor.close()
    conn.close()
    root.mainloop()


  
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import mysql.connector
from tkinter import Frame, Label, RIDGE, CENTER, LEFT, StringVar

def guerison():
    def get_connection():
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="formulaire"
            )
            return conn
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur de connexion", f"Erreur MySQL: {err}")
            return None

    def formulaire_guerison(utilisateur_id):
        conn = get_connection()
        if conn is None:
            return
            
        cursor = conn.cursor()
        
        try:
            # Récupérer les infos de base de l'utilisateur
            cursor.execute("SELECT nom, prenom FROM utilisateurs WHERE id = %s", (utilisateur_id,))
            utilisateur = cursor.fetchone()
            if utilisateur is None:
                messagebox.showerror("Erreur", "Utilisateur non trouvé")
                conn.close()
                return
                
            nom = utilisateur[0]
            prenom = utilisateur[1]

            # Vérifier si l'utilisateur a déjà des données de guérison
            cursor.execute("SELECT date_debut_traitement, date_fin_guerison, etat_sante_actuel, "
                          "symptomes_persistants, traitement_en_cours, etat_guerison "
                          "FROM guerison WHERE utilisateur_id = %s", (utilisateur_id,))
            existing_data = cursor.fetchone()

            # Interface stylée
            window = tk.Tk()
            window.title("Formulaire de Guérison")
            window.geometry("800x600")
            window.configure(bg="#F5F5F5")

            frame = Frame(window, bg="white", bd=2, relief=RIDGE)
            frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=550, height=550)

            Label(frame, text="Formulaire de Guérison", font=("Times New Roman", 20, "bold"), 
                  bg="white", fg="dark blue").grid(row=0, column=0, columnspan=2, pady=20)

            # Champs utilisateur (lecture seule)
            Label(frame, text="Nom:", bg="white").grid(row=1, column=0, padx=20, pady=5, sticky="w")
            entry_nom = ttk.Entry(frame, width=30)
            entry_nom.insert(0, nom)
            entry_nom.config(state="readonly")
            entry_nom.grid(row=1, column=1, pady=5)
              
            Label(frame, text="", bg="white").grid(row=2, column=0, padx=20)
            Label(frame, text="Prénom:", bg="white").grid(row=3, column=0, padx=20, pady=5, sticky="w")
            entry_prenom = ttk.Entry(frame, width=30)
            entry_prenom.insert(0, prenom)
            entry_prenom.config(state="readonly")
            entry_prenom.grid(row=3, column=1, pady=5)
            
            # Pré-remplir les champs si des données existent
            if existing_data:
                date_debut = existing_data[0].strftime("%Y-%m-%d") if existing_data[0] else ""
                date_fin = existing_data[1].strftime("%Y-%m-%d") if existing_data[1] else ""
                etat_sante = existing_data[2] if existing_data[2] else ""
                symptomes = existing_data[3] if existing_data[3] else ""
                traitement = existing_data[4] if existing_data[4] else ""
                etat_guerison = existing_data[5] if existing_data[5] else "En Cours"
            else:
                date_debut = ""
                date_fin = ""
                etat_sante = ""
                symptomes = ""
                traitement = ""
                etat_guerison = "En Cours"

            # Champs de formulaire
            Label(frame, text="", bg="white").grid(row=4, column=0, padx=20)
            Label(frame, text="Date début traitement:", bg="white").grid(row=5, column=0, padx=20, pady=5, sticky="w")
            entry_date_debut = DateEntry(frame, width=20, font=("Times New Roman", 12), date_pattern="yyyy-MM-dd")
            if date_debut:
                entry_date_debut.set_date(date_debut)
            entry_date_debut.grid(row=5, column=1, pady=5)
            
            Label(frame, text="", bg="white").grid(row=6, column=0, padx=20)
            Label(frame, text="Date fin guérison:", bg="white").grid(row=7, column=0, padx=20, pady=5, sticky="w")
            entry_date_fin = DateEntry(frame, width=20, font=("Times New Roman", 12), date_pattern="yyyy-MM-dd")
            if date_fin:
                entry_date_fin.set_date(date_fin)
            entry_date_fin.grid(row=7, column=1, pady=5)
            
            Label(frame, text="", bg="white").grid(row=8, column=0, padx=20)
            Label(frame, text="État de santé actuel:", bg="white").grid(row=9, column=0, padx=20, pady=5, sticky="w")
            entry_etat_sante = ttk.Entry(frame, width=30)
            entry_etat_sante.insert(0, etat_sante)
            entry_etat_sante.grid(row=9, column=1, pady=5)
            
            Label(frame, text="", bg="white").grid(row=10, column=0, padx=20)
            Label(frame, text="Symptômes persistants:", bg="white").grid(row=11, column=0, padx=20, pady=5, sticky="w")
            entry_symptomes = ttk.Entry(frame, width=30)
            entry_symptomes.insert(0, symptomes)
            entry_symptomes.grid(row=11, column=1, pady=5)
            
            Label(frame, text="", bg="white").grid(row=12, column=0, padx=20)
            Label(frame, text="Traitement en cours:", bg="white").grid(row=13, column=0, padx=20, pady=5, sticky="w")
            entry_traitement = ttk.Entry(frame, width=30)
            entry_traitement.insert(0, traitement)
            entry_traitement.grid(row=13, column=1, pady=5)
            
            Label(frame, text="", bg="white").grid(row=14, column=0, padx=20)
            Label(frame, text="État final de guérison:", bg="white").grid(row=15, column=0, padx=20, pady=5, sticky="w")
            etat_guerison_var = StringVar(value=etat_guerison)
            frame_radio = Frame(frame, bg="white")
            frame_radio.grid(row=15, column=1, pady=5, sticky="w")
            ttk.Radiobutton(frame_radio, text="Guéri", variable=etat_guerison_var, value="Guéri").pack(side=LEFT, padx=5)
            ttk.Radiobutton(frame_radio, text="En Cours", variable=etat_guerison_var, value="En Cours").pack(side=LEFT, padx=5)
            ttk.Radiobutton(frame_radio, text="Non Guéri", variable=etat_guerison_var, value="Non Guéri").pack(side=LEFT, padx=5)

            def save_data():
                nonlocal existing_data
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

                try:
                    if existing_data:
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
                    messagebox.showinfo("Succès", "Les informations de guérison ont été enregistrées avec succès.")
                    window.destroy()
                except mysql.connector.Error as err:
                    messagebox.showerror("Erreur MySQL", f"Erreur lors de l'enregistrement: {err}")
                finally:
                    conn.close()

            tk.Button(frame, text="Enregistrer", font=("Times New Roman", 15), bg="dark blue", fg="white",
                      command=save_data).grid(row=16, column=1, columnspan=2, pady=20)

            window.mainloop()

        except mysql.connector.Error as err:
            messagebox.showerror("Erreur MySQL", f"Erreur lors de la récupération des données: {err}")
            conn.close()

    # Fenêtre principale avec tableau des utilisateurs et leurs états de guérison
    main_window = tk.Tk()
    main_window.title("Liste des Patients et leur État de Guérison")
    main_window.geometry("1200x600")
    main_window.config(bg="#F5F5F5")

    # Frame pour le tableau
    frame_table = Frame(main_window, bg="white", bd=2, relief=RIDGE)
    frame_table.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

    # Titre
    Label(frame_table, text="Liste des Patients et leur État de Guérison - Sélectionnez un patient", 
          font=("Arial", 14, "bold"), bg="white").pack(pady=10)

    # Treeview pour afficher les utilisateurs et leurs infos de guérison
    tree = ttk.Treeview(frame_table, columns=("ID", "Prénom", "Nom", "Date Naissance", "Sexe", 
                                            "Début Traitement", "Fin Guérison", "État Guérison"), 
                       show="headings")
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Configuration des colonnes
    columns = [
        ("ID", 80), ("Prénom", 100), ("Nom", 100), 
        ("Date Naissance", 100), ("Sexe", 80),
        ("Début Traitement", 120), ("Fin Guérison", 120), 
        ("État Guérison", 100)
    ]
    
    for col, width in columns:
        tree.heading(col, text=col)
        tree.column(col, width=width, anchor=CENTER)

    # Remplir le tableau avec les données de la base de données
    def load_users():
        conn = get_connection()
        if conn is None:
            return
            
        cursor = conn.cursor()
        
        try:
            # Requête pour joindre les tables utilisateurs et guerison
            cursor.execute('''SELECT u.id, u.prenom, u.nom, u.date_naissance, u.sexe, 
                             g.date_debut_traitement, g.date_fin_guerison, g.etat_guerison
                             FROM utilisateurs u
                             LEFT JOIN guerison g ON u.id = g.utilisateur_id''')
            
            for row in tree.get_children():
                tree.delete(row)
                
            for user in cursor.fetchall():
                # Formater les dates pour l'affichage
                date_debut = user[5].strftime("%Y-%m-%d") if user[5] else ""
                date_fin = user[6].strftime("%Y-%m-%d") if user[6] else ""
                etat = user[7] if user[7] else "Non renseigné"
                
                tree.insert("", tk.END, values=(
                    user[0], user[1], user[2], 
                    user[3].strftime("%Y-%m-%d") if user[3] else "", 
                    user[4], 
                    date_debut, 
                    date_fin, 
                    etat
                ))
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur MySQL", f"Erreur lors du chargement des données: {err}")
        finally:
            conn.close()

    # Bouton de chargement
    btn_load = tk.Button(frame_table, text="Actualiser la liste", command=load_users, 
                         bg="blue", fg="white", font=("Arial", 10))
    btn_load.pack(pady=5)

    # Bouton pour ouvrir le formulaire de guérison
    def open_guerison_form():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner un patient")
            return
        user_data = tree.item(selected_item)['values']
        user_id = user_data[0]
        main_window.destroy()
        formulaire_guerison(user_id)

    btn_select = tk.Button(frame_table, text="Modifier/Remplir formulaire de guérison", command=open_guerison_form,
                          bg="green", fg="white", font=("Arial", 12, "bold"))
    btn_select.pack(pady=10)

    # Charger les utilisateurs au démarrage
    load_users()

    main_window.mainloop()












import webbrowser
from tkinter import Tk, Label, Canvas, Toplevel
from tkinter import ttk
from PIL import Image, ImageTk  # Pour gérer les images
def ouvrir_interface_web():
    # Remplace cette URL par celle de ton serveur local ou distant
    webbrowser.open("http://localhost/MedVisualisation/projetSite.php")
def menu_personnes_inscrites():
    # Création de la fenêtre secondaire avec Toplevel pour éviter les conflits avec Tk()
    window = Toplevel()
    window.title("Menu Utilisateur")
    window.geometry("800x700")
    window.resizable(False, False)  # Empêcher le redimensionnement

    # Charger et ajuster l'image de fond
    image_fond = Image.open("medical.png")
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
    btn_siteweb = ttk.Button(window, text="Accéder à l'interface Web", style="TButton", command=ouvrir_interface_web)
    btn_siteweb.place(relx=0.5, rely=0.7, anchor="center", width=500)
    btn_modifier = ttk.Button(window, text="Modifier les  informations", style="TButton", command=modifier)
    btn_modifier.place(relx=0.5, rely=0.4, anchor="center", width=500)
    
    btn_suprimer = ttk.Button(window, text="supprimer personne", style="TButton", command=supprimer_container)
    btn_suprimer.place(relx=0.5, rely=0.5, anchor="center", width=500)

    btn_guerison = ttk.Button(window, text="Remplir le formulaire de guérison", style="TButton", command=guerison)
    btn_guerison.place(relx=0.5, rely=0.6, anchor="center", width=500)
    

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

def main_menu():
    root = Tk()
    root.title("Menu Principal")
    root.geometry("800x700")
    root.resizable(False, False)

    # Charger l'image de fond
    image = Image.open("image.png")

    # Créer un Canvas et y ajouter l'image
    canvas = Canvas(root, width=800, height=700)
    canvas.pack(fill="both", expand=True)

    # Initialiser l'image de fond
    photo = ImageTk.PhotoImage(image.resize((800, 700)))
    canvas.create_image(0, 0, image=photo, anchor="nw")
    canvas.image = photo  # garder une référence

    # Créer les éléments à afficher sur l'image de fond
    label_titre = Label(root, text="Menu Principal", font=("Arial", 16, "bold"), fg="blue", bg="white")
    label_bien = Label(root, text="Bienvenue sur notre application de gestion du personnel",
                    font=("Helvetica", 14, "bold"), fg="#333", bg="white")

    style = ttk.Style()
    style.configure("TButton", font=("Arial", 14, "bold"), padding=10, background="white")

    btn_ajouter = ttk.Button(root, text="s'inscrire", style="TButton", command=ajouter_patien)
    btn_ajouter.place(relx=0.5, rely=0.4, anchor="center", width=500)

    btn_connecter = ttk.Button(root, text="se connester", style="TButton", command=menu_personnes_inscrites)
    btn_connecter.place(relx=0.5, rely=0.5, anchor="center", width=500)

    # Ajouter les éléments dans le Canvas pour qu’ils apparaissent par-dessus l’image
   

    # Redimensionnement dynamique de l’image
    def resize_image(event):
        new_width = event.width
        new_height = event.height
        resized = image.resize((new_width, new_height))
        new_photo = ImageTk.PhotoImage(resized)
        canvas.create_image(0, 0, image=new_photo, anchor="nw")
        canvas.image = new_photo

    root.bind("<Configure>", resize_image)

    root.mainloop()

# Programme principal
if __name__ == "__main__":
    # Fonctions factices pour tester
    

    

    main_menu()



  