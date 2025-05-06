from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector
import re
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
# Classe Formulaire (avec ajout de l'envoi d'email)
##########################################################################

class Formulaire:
    def __init__(self, root):
        self.root = root
        self.root.title("Formulaire d'inscription")
        self.root.geometry("800x600")
        self.root.configure(bg="#F5F5F5")

        # Création de la base de données et table si elles n'existent pas
        self.creer_base_et_table()

        # Cadre principal
        frame1 = Frame(root, bg="white", bd=2, relief=RIDGE)
        frame1.place(relx=0.5, rely=0.5, anchor=CENTER, width=500, height=550)

        # Titre
        Label(frame1, text="Formulaire d'inscription", font=("Times New Roman", 20, "bold"), 
              bg="white", fg="dark blue").grid(row=1, column=1, columnspan=4, pady=15)

        # Champs du formulaire
        champs = [
            ("Prénom:", 2), ("Nom:", 4), ("Date de naissance:", 6),
            ("Sexe:", 8), ("Numéro de téléphone:", 10), ("Email:", 12)
        ]

        for texte, row in champs:
            Label(frame1, text=texte, bg="white").grid(row=row, column=0, padx=20, pady=5, sticky=W)

        # Entrées
        self.entry_prenom = ttk.Entry(frame1, width=30)
        self.entry_prenom.grid(row=2, column=1, pady=5)

        self.entry_nom = ttk.Entry(frame1, width=30)
        self.entry_nom.grid(row=4, column=1, pady=5)

        self.date_entry = DateEntry(frame1, width=20, font=("Times New Roman", 12), 
                                  date_pattern="yyyy-MM-dd")
        self.date_entry.grid(row=6, column=1, pady=5)

        self.gender = StringVar()
        frame_gender = Frame(frame1, bg="white")
        frame_gender.grid(row=8, column=1, pady=5)
        ttk.Radiobutton(frame_gender, text="Masculin", variable=self.gender, value="Masculin").pack(side=LEFT, padx=10)
        ttk.Radiobutton(frame_gender, text="Féminin", variable=self.gender, value="Féminin").pack(side=LEFT, padx=10)

        self.entry_numeroTel = ttk.Entry(frame1, width=30)
        self.entry_numeroTel.grid(row=10, column=1, pady=5)

        self.entry_email = ttk.Entry(frame1, width=30)
        self.entry_email.grid(row=12, column=1, pady=5)
        self.entry_email.bind("<KeyRelease>", self.verifier_email)

        # Bouton d'enregistrement
        Button(frame1, text="Enregistrer", font=("Times New Roman", 15), 
              bg="dark blue", fg="white", command=self.enregistrer_donnees)\
              .grid(row=14, column=1, pady=20)

    def creer_base_et_table(self):
        """Crée la base de données et la table si elles n'existent pas"""
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
        """Vérifie si l'email saisi est valide"""
        email = self.entry_email.get()
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        self.entry_email.config(foreground="black" if re.match(pattern, email) else "red")

    def enregistrer_donnees(self):
        """Enregistre les données et envoie l'email de confirmation"""
        # Récupération des données
        prenom = self.entry_prenom.get()
        nom = self.entry_nom.get()
        date_naissance = self.date_entry.get()
        sexe = self.gender.get()
        numero_tel = self.entry_numeroTel.get()
        email = self.entry_email.get()

        # Validation des données
        if not all([prenom, nom, date_naissance, sexe, numero_tel, email]):
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis !", parent=self.root)
            return

        if not re.match(r"^\d{10}$", numero_tel):
            messagebox.showerror("Erreur", "Numéro de téléphone invalide !", parent=self.root)
            return

        try:
            con = mysql.connector.connect(host='localhost', user='root', password='', database='formulaire')
            mycur = con.cursor()
            
            # Vérification email existant
            mycur.execute("SELECT * FROM utilisateurs WHERE email = %s", (email,))
            if mycur.fetchone():
                messagebox.showerror("Erreur", "Cet email est déjà utilisé !", parent=self.root)
                return

            # Insertion dans la base
            mycur.execute("""
                INSERT INTO utilisateurs (prenom, nom, date_naissance, sexe, numero_tel, email) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (prenom, nom, date_naissance, sexe, numero_tel, email))
            con.commit()

            # Récupération de l'ID généré
            mycur.execute("SELECT id FROM utilisateurs WHERE email = %s", (email,))
            utilisateur_id = mycur.fetchone()[0]
            
            # ENVOI DE L'EMAIL DE CONFIRMATION
            envoyer_email_confirmation(email, utilisateur_id)
            
            con.close()

            # Affichage du message de succès avec l'ID
            messagebox.showinfo(
                "Succès", 
                f"Inscription réussie !\nVotre ID utilisateur est : {utilisateur_id}\n"
                f"Un email de confirmation a été envoyé à {email}",
                parent=self.root
            )

            # Fermeture de la fenêtre après inscription
            self.root.destroy()

        except mysql.connector.Error as e:
            messagebox.showerror("Erreur", f"Erreur de base de données : {e}", parent=self.root)

##########################################################################
# Programme principal
##########################################################################

if __name__ == "__main__":
    root = Tk()
    app = Formulaire(root)
    root.mainloop()
