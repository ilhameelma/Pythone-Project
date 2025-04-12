from tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.geometry("800x600")

# 1. Ouvrir l'image de fond
image = Image.open("C:\\Users\hp\\Desktop\\Bureau\\tp_data\\capture.PNG")  # Mets ici le nom exact de ton image

# 2. Redimensionner à la taille de la fenêtre
image = image.resize((800, 600))

# 3. Ajouter l'opacité (transparence)
image = image.convert("RGBA")  # Important : RGBA pour permettre la transparence
r, g, b, a = image.split()
# Réduire l'opacité en gardant une image visible (valeur entre 0 et 255)
opacity = 180  # Plus bas = plus transparent. Teste avec 180 ou 200 d'abord
a = a.point(lambda i: opacity)
image = Image.merge("RGBA", (r, g, b, a))

# 4. Convertir pour Tkinter
background_image = ImageTk.PhotoImage(image)

# 5. Créer un canvas avec image en fond
canvas = Canvas(root, width=800, height=600)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_image, anchor="nw")

# 6. Ajouter du contenu au-dessus
label = Label(root, text="Formulaire", font=("Arial", 20), bg="white")
canvas.create_window(400, 100, window=label)

root.mainloop()
