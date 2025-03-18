from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector
import re

class Formulaire:
    def __init__(self, root):
        self.root = root
        self.root.title("Formulaire")
        self.root.geometry("800x600")
        self.root.configure(bg="#F5F5F5")

        # Connexion MySQL et création de la base/table
        self.creer_base_et_table()

        # Cadre principal
        frame1 = Frame(root, bg="white", bd=2, relief=RIDGE)
        frame1.place(relx=0.5, rely=0.5, anchor=CENTER, width=500, height=550)

        # Titre
        Label(frame1, text="Formulaire", font=("Times New Roman", 20, "bold"), bg="white", fg="dark blue").grid(row=1, column=1, columnspan=4, pady=15)

        # Champs de formulaire
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
        ttk.Radiobutton(frame_gender, text="Masculin", variable=self.gender, value="Masculin").pack(side=LEFT, padx=10)
        ttk.Radiobutton(frame_gender, text="Féminin", variable=self.gender, value="Féminin").pack(side=LEFT, padx=10)
        abelVide=Label(frame1, text="",bg="white").grid(row=9, column=0, padx=20)  # Espacement vertical
        Label(frame1, text="Numéro de téléphone:", bg="white").grid(row=10, column=0, padx=20, pady=5, sticky=W)
        self.entry_numeroTel = ttk.Entry(frame1, width=30)
        self.entry_numeroTel.grid(row=10, column=1, pady=5)
        abelVide=Label(frame1, text="",bg="white").grid(row=11, column=0, padx=20)  # Espacement vertical
        Label(frame1, text="Email:", bg="white").grid(row=12, column=0, padx=20, pady=5, sticky=W)
        self.entry_email = ttk.Entry(frame1, width=30)
        self.entry_email.grid(row=12, column=1, pady=5)
        self.entry_email.bind("<KeyRelease>", self.verifier_email)

        # Boutons
        Button(frame1, text="Enregistrer", font=("times new roman", 15), bg="dark blue", fg="white", command=self.enregistrer_donnees).grid(row=14, column=1, pady=20)
    
    def creer_base_et_table(self):
        """ Crée la base de données et la table si elles n'existent pas """
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
        """ Vérifie si l'email entré est valide et change la couleur du texte """
        email = self.entry_email.get()
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        self.entry_email.config(foreground="black" if re.match(pattern, email) else "red")

    def enregistrer_donnees(self):
        """ Insère les données dans MySQL """
        prenom, nom, date_naissance, sexe, numero_tel, email = (
            self.entry_prenom.get(),
            self.entry_nom.get(),
            self.date_entry.get(),
            self.gender.get(),
            self.entry_numeroTel.get(),
            self.entry_email.get(),
        )

        if not all([prenom, nom, date_naissance, sexe, numero_tel, email]):
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis !", parent=self.root)
            return

        if not re.match(r"^\d{10}$", numero_tel):
            messagebox.showerror("Erreur", "Numéro de téléphone invalide !", parent=self.root)
            return

        try:
            con = mysql.connector.connect(host='localhost', user='root', password='', database='formulaire')
            mycur = con.cursor()
            # Vérifier si l'email existe déjà
            mycur.execute("SELECT * FROM utilisateurs WHERE email = %s", (email,))
            if mycur.fetchone():
                messagebox.showerror("Erreur", "tu as deja inscrit !", parent=self.root)
                return
            # Vérifier si le prénom et le nom existent déjà
            mycur.execute("SELECT * FROM utilisateurs WHERE nom = %s AND prenom = %s", (nom, prenom))
            if mycur.fetchone():
                messagebox.showinfo("Succès", "Tu as déjà inscrit !", parent=self.root)
                return
            
            mycur.execute("INSERT INTO utilisateurs (prenom, nom, date_naissance, sexe, numero_tel, email) VALUES (%s, %s, %s, %s, %s, %s)",
                          (prenom, nom, date_naissance, sexe, numero_tel, email))
            con.commit()
            con.close()

            messagebox.showinfo("Succès", "Ajout effectué !", parent=self.root)

        except mysql.connector.Error as e:
            messagebox.showerror("Erreur", f"Erreur de connexion : {e}", parent=self.root)

root = Tk()
obj = Formulaire(root)
root.mainloop()
