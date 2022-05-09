###############################################
# IN200 : projet d'informatique du second semestre
# PROJET : simulation d'un boulier "soroban"
# Auteurs : FABRET Sophie - FOURCADE Capucine - MANGNAN Maxime - REGGANE Dillan 
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
nb_boules=5 
nb_total_de_boules=0
centre_quinaire=42 
centre_unaire=222

# Initialisation de listes 
### Listes d'objets 
liste_boules=[]
liste_ligne=[]
liste_virgules=[]
liste_label=[]
liste_boules_à_traiter=[]
### Listes de coordonnées
liste_coordonnees=[]
liste_coordonnees_initiales=[]
### Listes servant au descriptif de l'état des boules 
liste_position_boules=[]
liste_boule_active=[]
liste_decimales=[0]*(nb_colonnes+1)

# Initialisation de comptes à rebours pour les appels récursifs de fonctions 
id_after=0

# Vitesse initiale de déplacement des boules & déplacement unitaire
v=20
dy=85

# Opérande des opérations
operande1=0
opérande2=0

################################################
### LES FONCTIONS
# Création du boulier
def creer_boulier():
    """Création du boulier (lignes & colonnes) par appel des fonctions : 
    * creer_colonnes 
    * creer_boules
    * afficher_chiffre_decimal_initialisation """
    creer_colonnes()
    creer_boules()
    afficher_chiffre_decimal_initialisation()

def creer_colonnes():
    """Créer les colonnes du boulier dans le canevas
    * création de lignes verticales à intervalles réguliers grâce à une boucle "for"
    * mémorisation des colonnes dans la liste : "liste_ligne" """
    global LARGEUR, nb_colonnes, c, line, virgule, liste_ligne, liste_virgules
    c = LARGEUR//(nb_colonnes+1)
    for i in range (1,nb_colonnes+1):
        line = canvas.create_line(i*c,10,i*c,HAUTEUR,fill="red",width=5)
        liste_ligne.append(line)
        afficher_chiffre_decimal(i*c)
        if i%3==0:
            virgule= canvas.create_oval((i*c-3,168), (i*c+3,175), fill="black")
            liste_virgules.append(virgule)

def creer_boules():
    """ * Création des boules dans le canevas et leur positionnement par deux boucles imbriquées (colonne x ligne)
    * Initialisation des listes concernant les attributs des boules:
     1) coordonnées (liste_coordonnees)
     2) position (listes_position_boules)
     3) caractère inactif de la boule (liste_boule_active) """
    global LARGEUR, nb_colonnes, nb_total_de_boules, liste_boules, liste_coordonnees, liste_position_boules, liste_position_boules_initiale, liste_boule_active, liste_coordonnees_initiales, c
    nb_total_de_boules=nb_colonnes*nb_boules
    c = LARGEUR//(nb_colonnes+1)
    h = HAUTEUR//7
    for i in range (1,nb_colonnes+1):
        for j in range(1,nb_boules+1):
            if j==1:
                boule = canvas.create_oval((i*c-20,centre_quinaire-20),(i*c+20,centre_quinaire+20),fill="red")
                liste_coordonnees.append(canvas.coords(boule))
                liste_boules.append(boule)
                liste_position_boules.append((i-1)%(nb_colonnes+1)*7)
            else : 
                boule = canvas.create_oval((i*c-20,(j-1)*h+centre_unaire-20),(i*c+20,(j-1)*h+centre_unaire+20),fill="red")
                liste_coordonnees.append(canvas.coords(boule))
                liste_boules.append(boule)
                liste_position_boules.append(((j%(nb_boules+1)+1)+(i-1)*7))
    liste_position_boules_initiale=list(liste_position_boules)
    liste_coordonnees_initiales=copy.deepcopy(liste_coordonnees)
    liste_boule_active=[0]*nb_total_de_boules

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
        if liste_coordonnees[i][0]<X<liste_coordonnees[i][2] and liste_coordonnees[i][1]<Y<liste_coordonnees[i][3]: 
            boules_à_traiter(i)
            canvas.itemconfigure(liste_boules[liste_boules_à_traiter[0][1]], fill="blue")
            mouvement_boules(0,len(liste_boules_à_traiter))

def initialise_liste_à_traiter (): 
    """Initialise la liste "liste_boule_à_traiter": redevient une liste vide """
    global liste_boules_à_traiter
    liste_boules_à_traiter=[]

def boules_à_traiter(i) :   
    """* Initialise la liste "liste_boules_à_traiter"
    * Détermine si la boule cliquée est une boule unaire 
     - Si oui : 
      -> détermine si elle est active ou désactive
      -> renvoie une liste contenant le numéro de la colonne de la boule, le numéro de la boule, 
     le déplcacement dy à effetuer (ou -dy suivant le cas actif/désactif), la valeur décimale 5 
     (ou -5 suivant le cas actif/désactif), le caractère actif/désactif (1/0) 
     -Sinon : appelle de la fonction "chercher_boules_unaires" pour connaître toutes les 
     boules unaires à déplacer """
    global liste_boules, liste_boule_active, liste_boules_à_traiter, boule_à_traiter
    initialise_liste_à_traiter()
    reste=i%5
    num_colonne=i//5+1
    boule_à_traiter=[]
    if reste==0: 
        if liste_boule_active[i]==0 : 
            boule_à_traiter=[num_colonne,i,dy,5,1]
            liste_boules_à_traiter.append(boule_à_traiter)
        else :
            boule_à_traiter=[num_colonne,i,-dy,-5,0]
            liste_boules_à_traiter.append(boule_à_traiter)
    else : 
        chercher_boules_unaires(num_colonne,i,reste)

def chercher_boules_unaires(num_colonne,i,reste) :
    """ * Cherche les boules unaires au-dessus/ en-dessous qui doivent être activées/désactivées
    * Renvoie une liste de liste : la liste contient des listes qui se compose du numéro de la 
    colonne d la boule sélectionnée, le numéro de la boule, le déplacement dy (ou -dy suivant le cas), 
    la valeur décimale 1 (ou -1 suiant le cas), le statut active/désactive"""
    global liste_boules, liste_boule_active, liste_boules_à_traiter
    if liste_boule_active[i] == 0 : 
        k=i-reste+1
        while liste_boule_active[k]==1: 
            k = k+1   
        for j in range (k,i+1):
            boule_à_traiter=[num_colonne,j,-dy,1,1]
            liste_boules_à_traiter.append(boule_à_traiter)
    else :
        k=5*num_colonne-1
        while liste_boule_active[k]==0:
            k-=1
        while k > (i-1):
            boule_à_traiter=[num_colonne,k,dy,-1,0]
            liste_boules_à_traiter.append(boule_à_traiter)
            k-=1

def mouvement_boules(j,max): 
    """* Met en mouvement les boules par appel récursif de la fonction avec la méthode (.after)
    * Le mouvement est décomposé en pas élémentaire dy/10 (ce qui permet de faire varier la vitesse)
    * Mise à jour des listes """
    global boule, liste_coordonnees_initiales, id_after, liste_coordonnees, liste_boules, v, liste_decimales, liste_boules_à_traiter
    dy=liste_boules_à_traiter[j][2]
    i=liste_boules_à_traiter[j][1]
    colonne_active=liste_boules_à_traiter[j][0]
    canvas.move(liste_boules[i],0,dy/10)
    liste_coordonnees[i]=canvas.coords(liste_boules[i])
    if liste_coordonnees[i][3]==liste_coordonnees_initiales[i][3]+dy or liste_coordonnees[i][3]==liste_coordonnees_initiales[i][3]:
        liste_position_boules[i]=liste_boules_à_traiter[j][4]
        liste_boule_active[i]=liste_boules_à_traiter[j][4]
        canvas.itemconfigure(liste_boules[i], fill="red")
        liste_decimales[colonne_active-1]+=liste_boules_à_traiter[j][3]
        afficher_chiffre_decimal(colonne_active,valeur=liste_decimales[colonne_active-1])
        canvas.after_cancel(id_after)
        j+=1
        if j<max:
            canvas.itemconfigure(liste_boules[liste_boules_à_traiter[j][1]], fill="blue")
            id_after = canvas.after(v, lambda : mouvement_boules(j,max))
    else : 
        id_after = canvas.after(v, lambda : mouvement_boules(j,max))

# Option de réinitialisation
def reinitialiser() : 
    """Réinitialise le boulier : toutes les boules sont désactivées"""
    global v, boule, line, liste_ligne, nb_total_de_boules, liste_position_boules, LARGEUR, nb_colonnes, liste_boules, liste_coordonnees, liste_boule_active, liste_decimales
    supprime_boules()
    supprime_colonnes()
    supprime_chiffre_decimal()
    liste_boules=[]
    liste_coordonnees=[]
    liste_ligne=[]
    liste_boule_active=[]
    liste_position_boules=[]
    LARGEUR=1200
    nb_colonnes=23
    liste_decimales=[0]*(nb_colonnes+1)
    v=20
    initialise_liste_à_traiter()
    creer_colonnes()
    creer_boules()
    afficher_chiffre_decimal_initialisation()

# Option "changement du nombre de colonne"
### Ajouter une colonne (+colonne)
def ajoute_colonne():
    """En cliquant sur le bouton "Ajout d'une colonne", une colonne est ajoutée à droite du boulier 
        * on supprime d'abord toutes les boules existantes
        * on supprime ensuite toutes les colonnes existantes
        * on supprime l'affichage de la valeur décimale de chaque colonne
        * on change le nombre de colonnes (+1) et la constante LARGEUR (+23)
        * on réinitialise toutes les listes
        * on appelle les fonctions : "creer_colonnes" et "creer_boules" pour créer le nouveau boulier"""
    global nb_colonnes, LARGEUR, liste_boules, liste_coordonnees, liste_ligne, liste_position_boules, liste_boule_active, liste_virgules, liste_label, liste_decimales
    supprime_boules()
    supprime_colonnes()
    supprime_chiffre_decimal()
    nb_colonnes+=1
    LARGEUR+=23
    liste_boules=[]
    liste_coordonnees=[]
    liste_boule_active=[]
    liste_ligne=[]
    liste_position_boules=[]
    liste_virgules=[]
    liste_label=[]
    liste_decimales=[0]*(nb_colonnes+1)
    creer_colonnes()
    creer_boules()
    afficher_chiffre_decimal_initialisation()
### Retirer une colonne
def enlève_colonne():
    """En cliquant sur le bouton "Enlève une colonne", alors 
    une colonne du boulier est supprimée
        * on supprime d'abord toutes les boules existantes
        * on supprime ensuite toutes les colonnes existantes
        * on supprime l'affichage de la valeur décimale de chaque colonne
        * on change le nombre de colonnes (-1) et la constante LARGEUR (-23)
        * on réinitialise toutes les listes
        * on appelle les fonctions : "creer_colonnes" et "creer_boules" pour créer le nouveau boulier"""
    global nb_colonnes, LARGEUR, liste_boules, liste_coordonnees, liste_ligne, liste_position_boules, liste_boule_active, liste_virgules, liste_decimales
    supprime_boules()
    supprime_colonnes()
    supprime_chiffre_decimal()
    nb_colonnes-=1
    LARGEUR-=23
    liste_boules=[]
    liste_coordonnees=[]
    liste_ligne=[]
    liste_boule_active=[]
    liste_position_boules=[]
    liste_virgules=[]
    liste_decimales=[0]*(nb_colonnes+1)
    creer_colonnes()
    creer_boules()
    afficher_chiffre_decimal_initialisation()
# Option "choisir une vitesse de déplacement des boules"
def variateur_vitesse():
    """Demande à l'utilisateur d'entrer une vitesse de déplacement des boules"""
    global v
    v=int(input("Choisir une vitesse de déplacement des boules"))

# Chiffres décimaux
### Affichage de la valeur décimale sous chacune des colonnes 
def afficher_chiffre_decimal_initialisation():
    """Initialise les chiffres décimaux du boulier : affichage "0" sous chaque colonne
       L'affichage est effectué par l'utilisation de label
       Ces labels sont mémorisés dans Liste_label afin de pouvoir les supprimer lors de 
       modification du nombre de colonnes ou de la réinitialisation du boulier"""
    global label,c, nb_colonnes, liste_label
    for i in range (1,nb_colonnes+1):
        label = tk.Label(racine, text="0", font=("helvetica", "10"))
        label.grid(row=HAUTEUR, column=i*c+1)
        liste_label.append(label) 
            
def afficher_chiffre_decimal(i, valeur=0):
    """Affiche la nouvelle valeur décimale d'une colonne après le mouvement de boules
       dans cette colonne.
       L'affichage est effectué par l'utilisation de label
       La Liste_label est mise à jour du nouvel affichage """
    global dec, label, c, nb_colonnes, liste_label
    dec=str(valeur)
    for j in range(nb_colonnes+1):
        if j==i:
            label = tk.Label(racine, text=dec, font=("helvetica", "10"))
            label.grid(row=HAUTEUR, column=i*c+1)
            liste_label.append(label)

#Option Opérations
### Affichage sur le boulier de l'équivalent d'un nombre décimal saisi par l'utilisateur
def saisie_entier():
    """Demande à l'utilisateur d'écrire un entier
    * Réinitialisation du boulier par appel de la fonction "reinitialiser"
    * Création de la liste boule à déplacer grâce à la fonction "creation_liste_boule_à_traiter_avec_decimale"
    *CHangement de couleur de la boule qui passe de rouge à bleu durant le déplacement
    * Appelle la fonction "mouvement_boule" afin que les boules à déplacer se déplacent"""
    global operande1, liste_boules_à_traiter, liste_boules
    operande1=int(input("Choisir un entier"))
    reinitialiser()
    creation_liste_boules_à_traiter_avec_decimale(operande1)
    canvas.itemconfigure(liste_boules[liste_boules_à_traiter[0][1]], fill="blue")
    mouvement_boules(0,len(liste_boules_à_traiter))

def calcul_equivalence_boulier(nombre): 
    """Affichage sur le boulier d'un nombre entier saisi par l'utilisateur selon l'algorithme suivant :
    - Calculer la longueur de l'entier saisi
    - Décomposition du nombre grâce à une boucle while (on traite les chiffres un à un en commençant par 
    celui des unités)
     -> Pour les quinaires : appel de la fonction "active_désactive_première_ligne_direct"
     -> Pour les unaires : appel de la fonction "active_partie_supérieure_direct" """
    global boule, dy, nb_colonnes, liste_boules, liste_boule_active
    colonne_active=nb_colonnes
    while nombre!=0:
        decimale_colonne=nombre%10
        num_quinaire=recuperation_numero_boule_quinaire(colonne_active)
        if decimale_colonne>4: 
            boule=liste_boules[num_quinaire]
            active_désactive_première_ligne_direct(num_quinaire) 
            decimale_colonne-=5
        if decimale_colonne!=0:
            active_partie_supérieure_direct(decimale_colonne,num_quinaire+decimale_colonne) 
        nombre=nombre//10
        colonne_active-=1

def creation_liste_boules_à_traiter_avec_decimale(nombre):
    """Trouve toutes les boules à traiter (c'est-à-dire à déplacer) et renvoie une liste contenant
    toutes les informations sur le statut des boules (liste : "liste_boule_à_traiter") """
    global liste_boules_à_traiter, boule_à_traiter, nb_colonnes
    colonne_active=nb_colonnes
    while nombre!=0:
        decimale_colonne_active=nombre%10
        num_quinaire=recuperation_numero_boule_quinaire(colonne_active)
        if decimale_colonne_active>4:
            boule_à_traiter=[colonne_active,num_quinaire,dy,5,1]
            liste_boules_à_traiter.append(boule_à_traiter)
            decimale_colonne_active-=5
        if decimale_colonne_active!=0:
            for j in range(num_quinaire+1, num_quinaire+decimale_colonne_active+1):
                boule_à_traiter=[colonne_active,j,-dy,1,1]
                liste_boules_à_traiter.append(boule_à_traiter)
        nombre=nombre//10
        colonne_active-=1

def opérations():
    """*Demande à l'utilisateur d'entrer une opération (addition, soustraction, multiplication)
    * calcul le résultat attendu avant d'appeler la fonction "calcul_equivalent_boulier" et "créer_
    liste_boule_addition" 
    * lance le mouvement des boules """
    global liste_boules_à_traiter, liste_boules
    s=input("Sairsir une opération (addition, soustraction, multiplication)")
    reinitialiser()
    sum=0
    Liste=list(s)
    if "+" in Liste :
        s=s.split("+")
        for i in range(len(s)): 
            sum+=int(s[i])
    elif "-" in Liste :
        s=s.split("-")
        sum=int(s[0])-int(s[1])
    elif "*" in Liste : 
        s=s.split("*")
        sum=int(s[0])*int(s[1])
    calcul_equivalence_boulier(int(s[0]))
    créer_liste_boule_addition(sum)
    if len(liste_boules_à_traiter) !=0 :
        canvas.itemconfigure(liste_boules[liste_boules_à_traiter[0][1]], fill="blue")
        mouvement_boules(0,len(liste_boules_à_traiter))

def créer_liste_boule_addition(nombre) :
    """ Récupère le résultat de l'opération voulue par l'utilisateur 
    * Décomposition de ce nombre et détermination des boules unaires/quinaires
    à déplacer grâce à des conditions "if" 
    * Constitution de la liste "liste_boule_à_traiter" """
    global liste_boules_à_traiter, liste_decimales, nb_colonnes, boule_à_traiter
    colonne_active=nb_colonnes
    while nombre!=0:
        decimale_colonne_active=nombre%10
        num_quinaire=recuperation_numero_boule_quinaire(colonne_active)
        if decimale_colonne_active>4:   
            if liste_boule_active[num_quinaire] ==0 :  
                boule_à_traiter=[colonne_active,num_quinaire,dy,5,1]
                liste_boules_à_traiter.append(boule_à_traiter)
                reste_unaire=liste_decimales[colonne_active-1]
            else :
                reste_unaire=liste_decimales[colonne_active-1]-5
        elif liste_boule_active[num_quinaire] ==1 :  
            boule_à_traiter=[colonne_active,num_quinaire,-dy,-5,0]
            liste_boules_à_traiter.append(boule_à_traiter)
            reste_unaire=liste_decimales[colonne_active-1]-5
        else : 
            reste_unaire=liste_decimales[colonne_active-1]
        reste=decimale_colonne_active%5
        difference=reste_unaire - reste
        if difference > 0: 
            j=num_quinaire+reste+difference
            while j>num_quinaire+reste:
                boule_à_traiter=[colonne_active,j,dy,-1,0]
                liste_boules_à_traiter.append(boule_à_traiter)
                j-=1
        else : 
            difference=abs(difference)
            j=num_quinaire+reste+difference
            for j in range (num_quinaire+reste_unaire+1,num_quinaire+reste_unaire+1+difference):
                boule_à_traiter=[colonne_active,j,-dy,1,1]
                liste_boules_à_traiter.append(boule_à_traiter)
        nombre=nombre//10
        colonne_active-=1
        difference=0
        reste=0
        reste_unaire=0

### Mouvement direct des boules : affiche le premier opérande 
def active_désactive_première_ligne_direct(i):
    """Si on clique sur une boule quinaire alors :
    * elle s'active si elle était désactivée
    * sinon elle se désactive
    Le mouvement se fait par appel de la fonction "mouvement_boule_quinaire" """
    canvas.itemconfigure(boule, fill="blue")
    if liste_boule_active[i] == 0:    
        liste_position_boules[i]=liste_position_boules[i]+1
        mouvement_boule_quinaire_direct(i,dy,1)
    else :
        liste_position_boules[i]=liste_position_boules[i]-1
        mouvement_boule_quinaire_direct(i,-dy,-1)    

def mouvement_boule_quinaire_direct(i,dy,position):
    """Met en mouvement une boule quinaire : 
    * le mouvement de chaque boule vaut dy :
     1) la boule quinaire se déplace vers le bas si l'utilisateur l'active
     2) dans le cas contraire, elle retrouve sa place originelle
    * après le mouvement de chacune des boules, les listes qui contiennent leurs attributs sont mises à jour"""
    global boule, id_after, v, liste_boules, liste_coordonnees_initiales, liste_decimales, liste_coordonnees
    canvas.move(boule,0,dy)
    liste_boules[i]=boule
    liste_coordonnees[i]=canvas.coords(liste_boules[i])
    canvas.itemconfigure(boule, fill="red")
    a=i//5
    liste_decimales[a]+=5*position
    afficher_chiffre_decimal(calcul_numéro_colonne(i),valeur=liste_decimales[a])
    liste_boule_active[i]+=position

def active_partie_supérieure_direct(reste, i):
    """Lorsque l'utilisateur clique sur une boule unaire inactive, alors les 
    boules non-actives au-dessus d'elle sont aussi activées et déplacées:
    * dans un premier temps, on recherche le numéro de la boule non-active la plus haute
    au-dessus de la boucle choisie
    * cette boule est mise en mouvemenent par l'appel de la fonction "mouvement_boule_unaire" """
    global boule, liste_boules, liste_boule_active
    k=i-reste+1  
    while liste_boule_active[k]==1: 
        k = k+1
    boule=liste_boules[k]
    canvas.itemconfigure(liste_boules[k], fill="blue")
    mouvement_boule_unaire_direct(k,-dy,1,i,-1)

def désactive_partie_inférieure_direct(i):
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
    mouvement_boule_unaire_direct(k,dy,-1,i,1)

def mouvement_boule_unaire_direct(i,dy,active, index, position):
    """Met en mouvement les boules unaires :
    * le mouvement de chaque boule vaut dy: 
     1) dans le cas d'une activation, toutes les boules unaires inactives au-dessus de celle choisie par l'utilisateur
    sont activées et remontées une à une en commençant par la plus haute
     2) dans le cas d'une désactivation, toutes les boules unaires actives en-dessous de celle choisie par l'utilisateur
    sont désactivées et descendues une à une en commençant par la plus basse
    * après le mouvement de chacune des boules, les listes qui contiennent leurs attributs sont mises à jour"""
    global boule, liste_coordonnees_initiales, id_after_unaire, liste_coordonnees, liste_boules, v, liste_decimales
    while (i < (index+1) and position==-1) or (i>index-1 and position==1):
        boule=liste_boules[i]
        canvas.itemconfigure(liste_boules[i], fill="blue")
        canvas.move(liste_boules[i],0,dy) 
        liste_coordonnees[i]=canvas.coords(liste_boules[i])
        liste_position_boules[i]=liste_position_boules[i]+position
        canvas.itemconfigure(liste_boules[i], fill="red")
        a=i//5
        liste_decimales[a]-=position
        afficher_chiffre_decimal(calcul_numéro_colonne(i),valeur=liste_decimales[a])
        liste_boule_active[i]-=position
        i -=position

# Fonctions de suppression d'éléments du canevas
def supprime_boules():
    """Supprime toutes les boules du boulier une à une"""
    global nb_total_de_boules
    for i in range(nb_total_de_boules):
        boule=liste_boules[i]
        canvas.delete(boule)

def supprime_colonnes():
    """Supprime toutes les colonnes du boulier une à une puis appelle la fonction "supprime_virgules" 
    pour effacer les marques de situation des chiffres"""
    global liste_ligne, nb_colonnes, line
    for i in range(nb_colonnes):
        line=liste_ligne[i]
        canvas.delete(line)
    supprime_virgules()

def supprime_virgules():  
    """Supprime toutes les marques de situation des chiffres situées sur la barre médiane"""  
    global liste_virgules
    for i in range(len(liste_virgules)):
            virgule=liste_virgules[i]
            canvas.delete(virgule)

def supprime_chiffre_decimal():
    """Supprime les labels utilisés pour l'affichage de la valeur décimale sous  chaque colonne""" 
    global label, nb_colonnes, liste_label, l
    compteur = len(liste_label)
    for i in range (compteur):
        l=liste_label[i]
        l.destroy()
    liste_label=[]

# Récupération de numéros  
def calcul_numéro_colonne(i):
    """Renvoie le numéro de la colonne de la boucle choisie par l'utilisateur"""
    numero_colonne=i//5+1
    return numero_colonne   

def recuperation_numero_boule_quinaire(numero_colonne):
    """"b"""
    numero_boule_quinaire=(numero_colonne-1)*5
    return numero_boule_quinaire

####################################################
### CREATION DE LA FENETRE RACINE
racine = tk.Tk()
canvas = tk.Canvas(racine, bg="black", width=LARGEUR, height=HAUTEUR)

# Structure du boulier
### Délimitation du boulier : cadre rectangulaire
canvas.create_line((0,0,0,HAUTEUR), fill="red", width=20)
canvas.create_line((0,0,LARGEUR,0), fill="red", width=20)
canvas.create_line((0,HAUTEUR,LARGEUR,HAUTEUR), fill="red", width=20)
canvas.create_line((LARGEUR,0,LARGEUR,HAUTEUR), fill="red", width=20)
### Ligne médiane qui permet la séparation entre les boules quinaires et les boules unaires 
barre_mediane= canvas.create_line((10,170),(LARGEUR-10,170),fill="white",width=20)
### Création du boulier : colonnes et boules 
boulier=creer_boulier()

# Déplacement direct des boules 
racine.bind("<Button-1>", coordonnees_boule)

# Création des widgets
bouton_reinitialiser=tk.Button(racine, text="Réinitialiser", activebackground="grey", command=reinitialiser)
bouton_colonne=tk.Button(racine, text="+ colonne", activebackground="grey", command=ajoute_colonne)
bouton_colonne_1=tk.Button(racine, text="- colonne", activebackground="grey", command=enlève_colonne)
bouton_vitesse=tk.Button(racine, text="Vitesse", activebackground="grey", command=variateur_vitesse)
bouton_operation=tk.Button(racine, text="Opérations", activebackground="grey", command=opérations)
bouton_saisie_entier=tk.Button(racine, text="Saisie entier", activebackground="grey", command=saisie_entier)

# Positionnement des widgets dans le canevas
canvas.grid(column=1, row=0, rowspan=HAUTEUR, columnspan=LARGEUR)
bouton_reinitialiser.grid(column=0, row=99)
bouton_colonne.grid(column=0, row=199)
bouton_colonne_1.grid(column=0, row=299)
bouton_vitesse.grid(column=0,row=399)
bouton_saisie_entier.grid(column=0,row=499)
bouton_operation.grid(column=0,row=599)

racine.mainloop()