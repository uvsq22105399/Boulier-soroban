# Boulier-soroban
INFORMATIQUE IN200
PROJET : « Boulier de Soroban » 
Auteurs : FABRET Sophie – FOURCADE Capucine – MANGNAN Maxime – REGGANE Dillan 
Rendu le : 09/05/2022
********************************************************************************************************************************************************************
L’objectif de ce projet est de simuler un boulier japonais (autrement appelé « boulier de Soroban ») à l’aide de l’interface graphique « tkinter ». Rappelons qu’un tel boulier est un abaque muni initialement de vingt-trois colonnes sur lesquelles sont disposées cinq boules de part et d’autre d’une barre médiane et avec lequel on peut effectuer des opérations de base de l’arithmétique (addition, soustraction, multiplication, division…). Notons également que sur chacune des colonnes (ou tiges), on trouve : 
-	Dans la partie supérieure à la ligne médiane, une boule quinaire à qui l’on attribue la valeur décimale de « 5 » lorsqu’elle est activée
-	Dans la partie inférieure, quatre boules unaires qui valent chacune « 1 » si elles sont activées. 
Une boule est activée par déplacement. L’ensemble des déplacements permet de réaliser les opérations attendues. 

Programme : 
        I- Représentation du boulier dans un canevas

La structure du boulier est générée dans une fenêtre racine de dimensions finies (largeur=1200 pixels et hauteur=600 pixels) grâce à la fonction « creer_boulier() ». Cette fonction positionne les colonnes, les boules et les valeurs décimales correspondant à chaque colonne au moyen de trois autres fonctions : 
-	creer_colonnes() : permet la création de vingt-trois colonnes blanches à intervalles réguliers ainsi que des points de marquage (ou virgules) sur la barre médiane qui aident à la visualisation
-	creer_boules() : crée et place les cent quinze boules du boulier sur chacune des colonnes précédemment dessinées. Elles sont initialement inactives. 
-	afficher_chiffre_decimal_initialisation : permet d’indiquer les valeurs décimales de chaque colonne. Des « 0 » apparaissent donc sous chaque colonne puisque à l’initialisation du boulier aucune boule n’est encore activée. 
Pour une question d’esthétisme, nous avons choisi de tracer un cadre rectangulaire afin de délimiter le boulier. Cette création, comme celle de la ligne médiane qui sépare boules unaires des boules quinaires, se fait en dehors de la fonction « creer_boulier ». 
        
        II- Déplacement des boules par manipulation directe ou clic de l’utilisateur 
Le programme lie le clic de gauche de la souris (avec racine.bind) à la fonction « coordonnees_boule ». Cette dernière permet de savoir si le clic de l’utilisateur dont on a enregistré les coordonnées est sur une boule ou non. Ce qui est possible par un encadrement avec les coordonnées disponibles de chaque boule dans la liste « liste_coordonnees ». 
-	Si le clic n’est pas sur une boule, alors il ne se passe rien. 
-	En revanche, dans le cas contraire, alors il y a déplacement : 
•	D’une seule boule, s’il s’agit d’une quinaire. 
•	D’une ou plusieurs boules, s’il s’agit d’une unaire (cela dépend des boules qui se trouvent en-dessous ou au-dessus de celle choisie et de leur statut actif/inactif). 
L’actionnement des boules est permis par la constitution d’une liste contenant les boules à déplacer (« liste_boule_à_traiter() ») qui se fait par l’appel de la fonction « boule_à_traiter ».  
L’activation/désactivation de la boule entraîne un changement de couleur de la boule et un déplacement suivant l’axe y qui vaut dy (85 pixels) si la boule descend (ce qui correspond à l’activation des quinaires et à la désactivation des unaires) ou –dy si la boule remonte (ce qui correspond à la désactivation des quinaires et à l’activation des unaires). 
Le mouvement des boules est réalisé par l’appel de la fonction récursive « mouvement_boules ». Le mouvement d’une boule se faisant par pas de dy/10. 
        
        III- Options proposées à l’utilisateur
Le programme propose différentes options à l’utilisateur au travers de boutons situés à gauche de la structure générale du boulier : 
1) « Réinitialiser » : permet à l’utilisateur de revenir à l’état initial du boulier, c’est-à-dire où toutes les boules sont inactives et sont au nombre de cent quinze. 
2) « + colonne » : un clic de l’utilisateur sur ce bouton permet de réinitialiser le boulier avant d’ajouter une colonne à droite du boulier. 
3) « - colonne » : un clic de l’utilisateur sur ce bouton permet de réinitialiser le boulier et d’ensuite lui retirer une colonne. 
4) « Vitesse » : un clic de l’utilisateur sur ce bouton permet à l’utilisateur d’entrer une vitesse de déplacement des animations. 
5) « Saisie entier » : un clic de l’utilisateur sur ce bouton permet à l’utilisateur d’entrer un entier qui s’affiche alors automatiquement sur le boulier ; le mouvement des boules est décomposé et s’effectue selon la vitesse initiale ou choisie par l’utilisateur
6) « Opérations » : un clic de l’utilisateur sur ce bouton permet à l’utilisateur d’entrer une opération (addition, soustraction, multiplication). Le boulier affiche directement le premier opérande. Puis l’opération est décomposée par une succession de mouvements de boules pour aboutir au résultat attendu. 
