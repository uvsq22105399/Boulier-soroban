 
###############################################
# PROJET : simulation d'un boulier "soroban"
# Auteurs : FABRET Sophie - Capucine Fourcade - MANGNAN Maxime - REGGANE Dillan 
# Date : 09/05/2022

###############################################
import tkinter as tk
import copy

### LES CONSTANTES
# Dimensions du canvas
LARGEUR = 1200
HAUTEUR = 600
# Structure générale du boulier initialement
nb_colonnes=23
nb_boules=5 # dans une colonne
nb_total_de_boules=0
centre_quinaire=42 #sert au positionnement des boules 
centre_unaire=222
# Initialisation de listes d'objets 
liste_boules=[]
liste_coordonnee=[]
liste_coordonnees_initiales=[]
liste_ligne=[]
couleur_boule=[]
liste_position_boules=[]
liste_boule_active=[]
# Comptes à rebours
id_after=0
id_after_unaire=0
# Vitesse initiale de déplacement des boules & déplacement unitaire
v=100
dy=85

################################################
### LES FONCTIONS
# Création du boulier
def creer_boulier():
    """Création du boulier par appel des fonctions 
    * creer_colonnes 
    * creer_boules"""
    creer_colonnes()
    creer_boules()

def creer_boules():
    """ * Création des boules dans le canevas et leur positionnement par deux boucles imbriquées (colonne x ligne)
    * Initialisation des listes concernant les attributs des boules:
     1) coordonnées 
     2) position 
     3) caractère inactif de la boule"""
    global LARGEUR, nb_colonnes, nb_total_de_boules, liste_boules, liste_coordonnee, couleur_boule, liste_position_boules, liste_position_boules_initiale, liste_boule_active, liste_coordonnees_initiales
    nb_total_de_boules=nb_colonnes*nb_boules
    couleur_boule=["red"]*nb_total_de_boules
    for i in range (1,nb_colonnes+1):
        c = LARGEUR//(nb_colonnes+1)
        for j in range(1,nb_boules+1):
            h = HAUTEUR//7
            if j==1:
                boule = canvas.create_oval((i*c-20,centre_quinaire-20),(i*c+20,centre_quinaire+20),fill="red")
                liste_coordonnee.append(canvas.coords(boule))
                liste_boules.append(boule)
                liste_position_boules.append((i-1)%(nb_colonnes+1)*7)
            else : 
                boule = canvas.create_oval((i*c-20,(j-1)*h+centre_unaire-20),(i*c+20,(j-1)*h+centre_unaire+20),fill="red")
                liste_coordonnee.append(canvas.coords(boule))
                liste_boules.append(boule)
                liste_position_boules.append(((j%(nb_boules+1)+1)+(i-1)*7))
    liste_position_boules_initiale=list(liste_position_boules)
    liste_coordonnees_initiales=copy.deepcopy(liste_coordonnee)
    liste_boule_active=[0]*nb_total_de_boules

def creer_colonnes():
    """Créer les colonnes du boulier dans le canevas
    * création de lignes verticales à intervalles réguliers
    * mémorisation des colonnes dans la liste : "liste_ligne" """
    global nb_colonnes, line, liste_ligne, LARGEUR
    for i in range (1,nb_colonnes+1):
        c = LARGEUR//(nb_colonnes+1)
        line = canvas.create_line(i*c,10,i*c,HAUTEUR,fill="red",width=5)
        liste_ligne.append(line)

# Option de réinitialisation
def reinitialiser() : 
    """Réinitialise le boulier : toutes les boules sont désactivées"""
    global boule, line, liste_ligne, nb_total_de_boules, liste_position_boules, LARGEUR, nb_colonnes, liste_boules, liste_coordonnee, liste_boule_active
    supprime_boules()
    supprime_colonnes()
    liste_boules=[]
    liste_coordonnee=[]
    liste_ligne=[]
    liste_boule_active=[]
    liste_position_boules=[]
    LARGEUR=1200
    nb_colonnes=23
    creer_colonnes()
    creer_boules()

# Mouvement des boules unaires/quinaires       
def coordonnees_boule(event):
    """Récupère les coordonnées du clic de la souris
    Si l'utilisateur clique sur une boule alors : 
    * la boule change d'état (actif/désactif) si c'est une boule quinaire
    * dans le cas d'une boule unaire : 
    - si elle était active, elle est désactivée ainsi que toutes les boules unaires en-dessous d'elle 
    (fontion: active_partie_inférieure)
    - sinon elle est activée ainsi que toutes les boules unaires au-dessus d'elle (fontion: 
    active_partie_supérieure)"""
    global boule, liste_boules, liste_boule_active
    X=event.x
    Y=event.y
    for i in range(nb_total_de_boules): 
        if liste_coordonnee[i][0]<X<liste_coordonnee[i][2] and liste_coordonnee[i][1]<Y<liste_coordonnee[i][3]: 
            boule = liste_boules[i]
            reste=i%5
            if reste==0:
                active_désactive_première_ligne(i)
            else :
                if liste_boule_active[i]==0:
                    active_partie_supérieure(reste,i)
                else : 
                    désactive_partie_inférieure(i)

def active_partie_supérieure(reste, i):
    """Lorsque l'utilisateur clique sur une boule unaire inactive, alors les 
    boules non-actives au-dessus d'elle sont aussi activées et déplacées:
    * dans un premier temps, on recherche le numéro de la boule non-active la plus haute
    au-dessus de la boucle choisie
    * cette boule est mise en mouvemenent par l'appel de la fonction "mouvement_boule_unaire" """
    global boule, liste_boules, liste_boule_active
    k=i-reste+1  
    while liste_boule_active[k]==1: #boule déjà active ne rien faire
        k = k+1
    boule=liste_boules[k]
    canvas.itemconfigure(liste_boules[k], fill="blue")
    couleur_boule[k]="blue"
    liste_boule_active[k]=1
    mouvement_boule_unaire(k,-dy,1,i,-1)

def désactive_partie_inférieure(i):
    """Lorsque l'utilisateur clique sur une boule unaire active pour la désastiver, alors les 
    boules actives en-dessous d'elle sont aussi désactivées et déplacées:
    * dans un premier temps, on recherche le numéro de la boule active la plus basse
    située au-dessous de la boucle choisie
    * cette boule est mise en mouvemenent par l'appel de la fonction "mouvement_boule_unaire" """
    global boule, liste_boules, liste_boule_active
    colonne=i//5+1
    k=5*colonne-1
    while liste_boule_active[k]==0:
        k-=1
    boule=liste_boules[k]
    canvas.itemconfigure(liste_boules[k], fill="blue")
    couleur_boule[k]="blue"
    liste_boule_active[k]=0
    mouvement_boule_unaire(k,dy,-1,i,1)

def active_désactive_première_ligne(i):
    """Si on clique sur une boule quinaire alors :
    * elle s'active si elle était désactivée
    * sinon elle se désactive
    Le mouvement se fait par appel de la fonction "mouvement_boule_quinaire" """
    canvas.itemconfigure(boule, fill="blue")
    couleur_boule[i]="blue"
    if liste_boule_active[i] == 0:    
        liste_boule_active[i]=1
        liste_position_boules[i]=liste_position_boules[i]+1
        mouvement_boule_quinaire(i,dy)
    else :
        liste_boule_active[i]=0
        liste_position_boules[i]=liste_position_boules[i]-1
        mouvement_boule_quinaire(i, -dy)

def mouvement_boule_quinaire(i,dy):
    """Met en mouvement une boule quinaire par appel récursif pour permmettre la modification de la vitesse des 
    animations : 
    * le mouvement de chaque boule est décomposé en 10 pas unitaires de longueur dy/10
    * la fonction se rappelle elle-même tant que la boule n'a pas atteint la coordonnée cible (utilisation d'un 
    compte à rebours avec la méthode .after qui intègre par ailleurs en paramètre la vistesse v de déplacement 
    des boules)
    * lorsque la boule a atteint la coordonnée cible, le compte à rebours est stoppé avec l'utilisation de la 
    méthode .after_cancel : 
     1) la boule quinaire se déplace vers le bas si l'utilisateur l'active
     2) dans le cas contraire, elle retrouve sa place originelle
    * durant le déplacement, les boules change de couleur avant de reprendre leur couleur initiale
    * après le mouvement de chacune des boules, les listes qui contiennent leurs attributs sont mises à jour"""
    global boule, id_after, v, liste_boules, liste_coordonnees_initiales
    canvas.move(boule,0,dy/10)
    liste_boules[i]=boule
    liste_coordonnee[i]=canvas.coords(liste_boules[i])
    if liste_coordonnee[i][3]==liste_coordonnees_initiales[i][3]+dy or liste_coordonnee[i][3]==liste_coordonnees_initiales[i][3]:
        canvas.itemconfigure(boule, fill="red")
        couleur_boule[i]="red"
        canvas.after_cancel(id_after)
    else :
        id_after = canvas.after(v, lambda : mouvement_boule_quinaire(i,dy))

def mouvement_boule_unaire(i,dy,active, index, position):
    """Met en mouvement les boules unaires par appel récursif pour permettre la modification
    de la vitesse des animations:
    * le mouvement de chaque boule est décomposé en 10 pas unitaires de longueur dy/10
    * la fonction se rappelle elle-même tant que la boule n'a pas atteint la coordonnée cible (utilisation d'un 
    compte à rebours avec la méthode .after qui intègre par ailleurs en paramètre la vistesse v de déplacement 
    des boules)
    * lorsque la boule a atteint la coordonnée cible, le compte à rebours est stoppé avec l'utilisation de la 
    méthode .after_cancel et la boule suivante est mise en mouvement : 
     - dans le cas d'une activation, toutes les boules unaires inactives au-dessus de celle choisie par l'utilisateur
    sont activées et remontées une à une en commençant par la plus haute
     - dans le cas d'une désactivation, toutes les boules unaires actives en-dessous de celle choisie par l'utilisateur
    sont désactivées et descendues une à une en commençant par la plus basse
     - la boule choisie par l'utilisateur arrête le mouvement après son déplacement 
    * durant le déplacement, les boules change de couleur avant de reprendre leur couleur initiale
    * après le mouvement de chacune des boules, les listes qui contiennent leurs attributs sont mises à jour"""
    global boule, liste_coordonnees_initiales, id_after_unaire, liste_coordonnee, liste_boules, v
    canvas.move(liste_boules[i],0,dy/10) 
    liste_coordonnee[i]=canvas.coords(liste_boules[i])
    if liste_coordonnee[i][3]==liste_coordonnees_initiales[i][3]+dy or liste_coordonnee[i][3]==liste_coordonnees_initiales[i][3]:
        liste_position_boules[i]=liste_position_boules[i]+position
        canvas.itemconfigure(liste_boules[i], fill="red")
        couleur_boule[i]="red"
        canvas.after_cancel(id_after_unaire)
        i -=position
        if (i < (index+1) and position==-1) or (i>index-1 and position==1):
            boule=liste_boules[i]
            canvas.itemconfigure(liste_boules[i], fill="blue")
            couleur_boule[i]="blue"
            liste_boule_active[i]-=position
            id_after_unaire = canvas.after(v, lambda : mouvement_boule_unaire(i,dy,active, index, position))
    else : 
        id_after_unaire = canvas.after(v, lambda : mouvement_boule_unaire(i,dy,active, index, position))

# Option "changement du nombre de colonne"
def ajoute_colonne():
    """En cliquant sur le bouton "Ajout d'une colonne", alors 
    une colonne à droite du boulier est ajoutée
    * on supprime d'abord toutes les boules existantes
    * on supprime ensuite toutes les colonnes existantes
    * on change le nombre de colonnes (+1) et la constante LARGEUR (+23)
    * on réinitialise toutes les listes
    * on appelle les fonctions : "creer_colonnes" et "creer_boules" pour créer le nouveau boulier"""
    global nb_colonnes, LARGEUR, liste_boules, liste_coordonnee, liste_ligne, liste_position_boules, liste_boule_active
    supprime_boules()
    supprime_colonnes()
    nb_colonnes+=1
    LARGEUR+=23
    if (len(liste_boules)!=0) :
        liste_boules=[]
    if (len(liste_coordonnee)!=0) :
        liste_coordonnee=[]
    if (len(liste_boule_active)!=0) :
        liste_boule_active=[]
    if (len(liste_ligne)!=0) :
        liste_ligne=[]
    if (len(liste_position_boules)!=0) :
        liste_position_boules=[]
    creer_colonnes()
    creer_boules()

def enlève_colonne():
    """En cliquant sur le bouton "Enlève une colonne", alors 
    une colonne du boulier est supprimée
    * on supprime d'abord toutes les boules existantes
    * on supprime ensuite toutes les colonnes existantes
    * on change le nombre de colonnes (-1) et la constante LARGEUR (-23)
    * on réinitialise toutes les listes
    * on appelle les fonctions : "creer_colonnes" et "creer_boules" pour créer le nouveau boulier"""
    global nb_colonnes, LARGEUR, liste_boules, liste_coordonnee, liste_ligne, liste_position_boules, liste_boule_active
    supprime_boules()
    supprime_colonnes()
    nb_colonnes-=1
    LARGEUR-=23
    liste_boules=[]
    liste_coordonnee=[]
    liste_ligne=[]
    liste_boule_active=[]
    liste_position_boules=[]
    creer_colonnes()
    creer_boules()

def supprime_boules():
    """Supprime toutes les boules du boulier une à une"""
    global nb_total_de_boules
    for i in range(nb_total_de_boules):
        boule=liste_boules[i]
        canvas.delete(boule)

def supprime_colonnes():
    """Supprime toutes les colonnes du boulier une à une"""
    global liste_ligne, nb_colonnes, line
    for i in range(nb_colonnes):
        line=liste_ligne[i]
        canvas.delete(line)

# Option "choisir une vitesse de déplacement des boules"
def variateur_vitesse():
    """Demande à l'utilisateur d'entrer une vitesse de déplacement des boules"""
    global v
    v=int(input("Choisir une vitesse de déplacement des boules"))


def opérations():
    global dy,boule, liste_coordonnees_initiales, id_after_unaire, liste_coordonnee, liste_boules, v, n, premier, deuxieme
    
    n=0
    m=0
    reinitialiser()
    premier= int(input('premier chiffre'))
    signe= input('signe')
    deuxieme= int(input('deuxième chiffre'))
    if signe=='+':
        opération_addition()

    if signe=='*':
        opération_multiplication()
        

def opération_addition(premier,deuxieme):
    global dy,boule, liste_coordonnees_initiales, id_after_unaire, liste_coordonnee, liste_boules, v, n, premier, deuxieme
    
       
    premier_str= str(premier)
    liste= list(premier_str)
    for i in range (0,len(premier_str)+1,-1):
        if int(liste[i])>5:
            mouvement_boule_quinaire(i)
            nmbre_unaire= int(liste[i])-5
            mouvement_boule_unaire(colonne i,déplacement de nmbre_unaire boules)
        else:
            mouvement_boule_unaire(colonne i, déplacement de int(liste[i]) boules)

    
    somme= premier+deuxieme
    somme_str= str(somme)
    liste2= list(somme_str)
    for i in range (0,len(somme_str)+1,-1):
        if int(liste2[i])>5:
            mouvement_boule_quinaire(i)
            nmbre_unaire2= int(liste[i])-5
            mouvement_boule_unaire(colonne i,déplacement de nmbre_unaire2 boules)
        else:
            mouvement_boule_unaire(colonne i, déplacement de int(liste2[i]) boules)







def opération_multiplication(premier,deuxieme):
    global dy,boule, liste_coordonnees_initiales, id_after_unaire, liste_coordonnee, liste_boules, v, n, premier, deuxieme

    







    

    

    

        
        
        
        


    
    
   

    









### CREATION DE LA FENETRE RACINE
racine = tk.Tk()
canvas = tk.Canvas(racine, bg="black", width=LARGEUR, height=HAUTEUR)
#label = tk.Label(racine, text="1", font=("helvetica", "10"))

# Délimitation du boulier
canvas.create_line((0,0,0,HAUTEUR), fill="red", width=20)
canvas.create_line((0,0,LARGEUR,0), fill="red", width=20)
canvas.create_line((0,HAUTEUR,LARGEUR,HAUTEUR), fill="red", width=20)
canvas.create_line((LARGEUR,0,LARGEUR,HAUTEUR), fill="red", width=20)
barre_mediane= canvas.create_line((10,170),(LARGEUR-10,170),fill="white",width=20)

# Déplacement des boules 
boulier=creer_boulier()
racine.bind("<Button-1>", coordonnees_boule)
# Création des widgets
bouton_reinitialiser=tk.Button(racine, text="Réinitialiser", activebackground="grey", command=reinitialiser)
bouton_colonne=tk.Button(racine, text="Ajout d'une colonne", activebackground="grey", command=ajoute_colonne)
bouton_colonne_1=tk.Button(racine, text="Enlève une colonne", activebackground="grey", command=enlève_colonne)
bouton_vitesse=tk.Button(racine, text="Variation vitesse", activebackground="grey", command=variateur_vitesse)
bouton_opérations=tk.Button(racine, text="Opérations", activebackground="grey", command=opérations)
# Positionnement des widgets
canvas.grid(column=0, row=0, columnspan=5)
#label.grid(row=0, column=0, columnspan=2)
bouton_reinitialiser.grid(column=0, row=1)
bouton_colonne.grid(column=1, row=1)
bouton_colonne_1.grid(column=2, row=1)
bouton_vitesse.grid(column=3,row=1)
bouton_opérations.grid(column=4, row=1)

racine.mainloop()
