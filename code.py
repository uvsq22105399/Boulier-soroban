
import tkinter as tk
import random as rd


#23lignes
LARGEUR = 1200
HAUTEUR = 600
racine = tk.Tk()
canvas = tk.Canvas(racine, bg="black", width=LARGEUR, height=HAUTEUR)

for i in range (24):
    c = LARGEUR//24
    line = canvas.create_line(i*c,10,i*c,600,fill='red',width=5)


line2 = canvas.create_line(0,0,0,HAUTEUR,fill='red',width=20)
line3 = canvas.create_line(0,0,LARGEUR,0,fill='red',width=20)
line4 = canvas.create_line(0,HAUTEUR,LARGEUR,HAUTEUR,fill='red',width=10)
line5 = canvas.create_line(LARGEUR,0,LARGEUR,HAUTEUR,fill='red',width=10)




for j in range (0, 1120, 50) :
    for i in range (40,560,112):
        rond= canvas.create_oval((35+j,30+i),(65+j,60+i),fill='red')


ligne_separation= canvas.create_line((10,150),(1195,150),fill='white',width=10)



canvas.grid()
canvas.pack()

racine.mainloop() 

import tkinter as tk
import random as rd


#23lignes
LARGEUR = 1200
HAUTEUR = 600
racine = tk.Tk()
canvas = tk.Canvas(racine, bg="black", width=LARGEUR, height=HAUTEUR)

for i in range (24):
    c = LARGEUR//24
    line = canvas.create_line(i*c,10,i*c,600,fill='red',width=5)


line2 = canvas.create_line(0,0,0,HAUTEUR,fill='red',width=20)
line3 = canvas.create_line(0,0,LARGEUR,0,fill='red',width=20)
line4 = canvas.create_line(0,HAUTEUR,LARGEUR,HAUTEUR,fill='red',width=10)
line5 = canvas.create_line(LARGEUR,0,LARGEUR,HAUTEUR,fill='red',width=10)




for j in range (0, 1120, 50) :
    for i in range (40,560,112):
        rond= canvas.create_oval((35+j,30+i),(65+j,60+i),fill='red')


ligne_separation= canvas.create_line((10,150),(1195,150),fill='white',width=10)



canvas.grid()
canvas.pack()

racine.mainloop()
