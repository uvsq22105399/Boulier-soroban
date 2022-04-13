import tkinter as tk
import random as rd


#23lignes
LARGEUR = 1200
HAUTEUR = 600
racine = tk.Tk()
canvas = tk.Canvas(racine, bg="black", width=LARGEUR, height=HAUTEUR)

for i in range (30, 1200, 52):
    line = canvas.create_line((int(i),10),(int(i),600),fill='red',width=5)

line2 = canvas.create_line(0,0,0,HAUTEUR,fill='red',width=20)
line3 = canvas.create_line(0,0,LARGEUR,0,fill='red',width=20)
line4 = canvas.create_line(0,HAUTEUR,LARGEUR,HAUTEUR,fill='red',width=10)
line5 = canvas.create_line(LARGEUR,0,LARGEUR,HAUTEUR,fill='red',width=10)

canvas.grid()
canvas.pack()

tk.mainloop()