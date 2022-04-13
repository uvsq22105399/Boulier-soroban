import tkinter as tk
import random as rd


#23lignes
LARGEUR = 1200
HAUTEUR = 600
racine = tk.Tk()
canvas = tk.Canvas(racine, bg="black", width=LARGEUR, height=HAUTEUR)

ligne = canvas.create()
for i in range (30, 1200, 52):
    line = canvas.create_line((int(i),10),(int(i),600),fill='red',width=5)



canvas.grid()
canvas.pack()

racine.mainloop()