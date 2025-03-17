from tkinter import *
from tkinter import filedialog, messagebox
from tkcalendar import DateEntry  

# Fonction pour sélectionner un fichier médical
def ajouter_fichier():
    fichier_path = filedialog.askopenfilename(title="Sélectionner un fichier médical",
                                              filetypes=[("Tous les fichiers", "*.*"), 
                                                         ("PDF", "*.pdf"), 
                                                         ("Images", "*.jpg;*.png"),
                                                         ("Documents", "*.docx;*.txt")])
    if fichier_path:
        fichier_label.config(text=f"Fichier sélectionné: {fichier_path}")

# Fonction pour afficher/masquer les champs en fonction des cases cochées
def afficher_entry(section, index):
    if sections[section]["variables"][index].get():  
        sections[section]["entries"][index].pack(side="left", padx=5)  # Afficher Entry
    else:
        sections[section]["entries"][index].pack_forget()  # Masquer Entry

# Fonction pour récupérer et afficher les données saisies
def submit():
    donnees = {}  
    for section, data in sections.items():
        donnees[section] = {}
        for i, var in enumerate(data["variables"]):
            if var.get():  
                texte = data["entries"][i].get()
                donnees[section][data["elements"][i]] = texte  

    fichier = fichier_label.cget("text").replace("Fichier sélectionné: ", "")
    
    if fichier == "":
        messagebox.showwarning("Avertissement", "Veuillez ajouter un fichier médical avant de soumettre.")
    else:
        messagebox.showinfo("Succès", "Les données et le fichier ont été enregistrés avec succès !")
        print("Fichier enregistré:", fichier)

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

