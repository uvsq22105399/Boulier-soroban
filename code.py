import tkinter as tk
import random as rd
###Constantes
LARGEUR = 1600
HAUTEUR = 900

racine = tk.Tk()
canvas = tk.Canvas(racine, bg="black", width=LARGEUR, height=HAUTEUR)
canvas.grid()
canvas.pack()

racine.mainloop()