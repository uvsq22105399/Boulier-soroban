###############################################
# PROJET : simulation d'un boulier "soroban"
# Auteurs : 

import tkinter as tk
import random as rd

### Constantes
# Dimensions du canvas
LARGEUR = 1200
HAUTEUR = 600
# Listes d'objets 
liste_boules=[]
liste_coordonnee=[]
couleur_boule=["red"]*115

### Fontions
def reinitialiser() : 
    """Réinitialise le boulier : toutes les boules sont désactivées"""
    for i in range(115):
        boule=liste_boules[i]
        canvas.itemconfigure(boule, fill="red")
        couleur_boule[i]="red"
        liste_boules[i]=boule

def coordonnees_balle(event):
    """Récupère les coordonnées du clic de la souris
    Si l'utilisateur clique sur une boule alors : 
    * la boule change d'état (actif/désactif) si c'est une boule quinaire
    * dans le cas d'une boule unaire : 
    - si elle était active, elle est désactivée ainsi que toutes les boules unaires en-dessous d'elle 
    (fontion: active_partie_inférieure)
    - sinon elle est activée ainsi que toutes les boules unaires au-dessus d'elle (fontion: 
    active_partie_supérieure)"""
    global boule
    X=event.x
    Y=event.y
    for i in range(115): 
        if liste_coordonnee[i][0]<X<liste_coordonnee[i][2] and liste_coordonnee[i][1]<Y<liste_coordonnee[i][3]: 
            boule = liste_boules[i]
            reste=i%5
            if reste==0:
                active_désactive_première_ligne(i)
            elif couleur_boule[i] == "red":
                active_partie_supérieure(reste,i)
            else : 
                active_partie_inférieure(i)

def active_partie_supérieure(reste, i):
    """Passage de rouge à bleu des parties supérieures unaires"""
    k=i-reste+1
    for j in range(k,i+1):
        boule=liste_boules[j]
        canvas.itemconfigure(boule, fill="blue")
        couleur_boule[j]="blue"
        liste_boules[j]=boule

def active_partie_inférieure(i):
    """Passage de bleu à rouge des parties inférieures unaires"""
    colonne=i//5+1
    k=5*colonne-1
    for j in range(i,k+1):
        boule=liste_boules[j]
        canvas.itemconfigure(boule, fill="red")
        couleur_boule[j]="red"
        liste_boules[j]=boule

def active_désactive_première_ligne(i):
    """b"""
    if couleur_boule[i] == "red":
        canvas.itemconfigure(boule, fill="blue")
        couleur_boule[i]="blue"
        liste_boules[i]=boule
    else :
        canvas.itemconfigure(boule, fill="red")
        couleur_boule[i]="red"
        liste_boules[i]=boule

### Création de la fenêtre racine
racine = tk.Tk()
canvas = tk.Canvas(racine, bg="black", width=LARGEUR, height=HAUTEUR)

# Délimitation du boulier
canvas.create_line((0,0,0,HAUTEUR), fill="red", width=20)
canvas.create_line((0,0,LARGEUR,0), fill="red", width=20)
canvas.create_line((0,HAUTEUR,LARGEUR,HAUTEUR), fill="red", width=20)
canvas.create_line((LARGEUR,0,LARGEUR,HAUTEUR), fill="red", width=20)
ligne_separation= canvas.create_line((10,150),(1190,150),fill="white",width=10)

# Création des lignes & des boules
for i in range (1, 24):
    c = LARGEUR//24
    line = canvas.create_line(i*c,10,i*c,600,fill="red",width=5)
    for j in range(1, 6):
        h = HAUTEUR//6
        boule = canvas.create_oval((i*c-20,j*h-20),(i*c+20,j*h+20),fill="red")
        liste_coordonnee.append(canvas.coords(boule))
        liste_boules.append(boule)
       
# Déplacement des boules 
racine.bind("<Button-1>", coordonnees_balle)
# Création des widgets
bouton_reinitialiser=tk.Button(racine, text="Réinitialiser", activebackground="grey", command=reinitialiser)
# Positionnement des widgets
bouton_reinitialiser.grid(column=0, row=2)
canvas.grid()

racine.mainloop()