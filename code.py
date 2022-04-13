import tkinter as tk
import random as rd

LARGEUR = 600
HAUTEUR = 600
racine = tk.Tk()
canvas = tk.Canvas(racine, bg="black", width=LARGEUR, height=HAUTEUR)
canvas.grid()
canvas.pack()

racine.mainloop()