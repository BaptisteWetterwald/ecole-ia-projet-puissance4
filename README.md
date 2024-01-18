Ce projet a été réalisé par Gauthier Cetingoz et Baptiste Wetterwald

#Introduction
Le script développé utilise l'algorithme alpha-beta pour la prise de décision dans le contexte du jeu de puissance 4.

La fonction principale, alpha_beta_decision, parcourt les mouvements possibles et appelle la fonction min_value pour évaluer les positions alternatives. Les variables alpha et beta sont utilisées pour effectuer l'élagage alpha-beta, limitant la recherche aux branches les plus prometteuses. Pendant cette itération, la meilleure valeur et le meilleur mouvement sont continuellement mis à jour.

#Explications
La fonction min_value représente le comportement du joueur MIN dans l'algorithme minimax. Elle évalue les conditions de victoire, la profondeur maximale, et explore davantage les mouvements possibles en appelant la fonction max_value. L'élagage alpha-beta est effectué en comparant la valeur obtenue avec alpha. De la même manière, max_value correspond au joueur MAX et compare le score à bêta.

La fonction eval évalue la position actuelle du jeu en utilisant la fonction compute_score pour chaque joueur. Elle retourne la différence entre le score du joueur actuel et celui de son adversaire.

Enfin, compute_score attribue des points en fonction des alignements réussis des pions du joueur actuel sur le plateau, prenant en compte les alignements horizontaux, verticaux et diagonaux.

#Les limites de notre IA
L'IA semble bien se débrouiller à partir du niveau de profondeur 4.

Cependant pour les niveaux inférieurs, nous avons remarqué un problème avec notre implémentation :
Si le joueur adverse a aligné 2 pions horizontalement et que les 2 côtés de ces pions seraient atteignables (voir ci-dessous), il peut poser un 3e pion en essayant de le centrer au maximum afin de garantir sa victoire au tour suivant (si l'autre joueur n'a pas de placement gagnant directement).

Ex : 

0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 2 0 0 0
0 0 1 1 0 0 0

Imaginons que cette grille représente l'état actuel du jeu et que ce soit le tour de J2.
Dans cette situation, il faudrait que l'IA joue à côté de l'un des deux 1 dans la grille.
Sinon, le joueur 1 n'aura qu'à jouer à côté de l'un de ses deux pions pour être sûr de gagner : si J2 joue à gauche, J1 jouera à droite et si J2 joue à droite, J1 jouera à gauche.

Ce problème est récurrent pour les lignes, il serait possible de "hardcoder" cette solution en vérifiant bien que les 2 côtés soient atteignables (non occupés et qu'il y ait un pion en-dessous) mais cela nous paraît superflu (le niveau 4 ne demandant pas un processeur très puissant pour jouer vite) en plus de ne pas être très élégant. Cette condition supplémentaire rallongerait le temps d'attente pour les niveaux >= 4 qui l'infèrent déjà.

En IA vs Humain, nous n'arrivons plus à gagner à partir du niveau 5.
En IA vs IA, elles arrivent toujours à égalité dès le niveau 4 (pour le niveau 3, c'est la situation évoquée précédemment qui met fin à la partie).

Nous avons voulu implémenter du parallélisme pour optimiser les calculs, d'abord avec des processus comme conseillé dans le sujet, mais nous avons rencontré un problème : la copie du board crée de nouvelles grilles vides et les affiche à l'écran, se superposant à la partie principale et mettant le thread principal en pause (il faut fermer les nouvelles fenêtres pour que le thread principal soit repris). 
Ensuite, nous avons tenté d'utiliser des threads plutôt que des processus : plus de fenêtres superflues qui s'ouvrent...

IA vs IA lvl 8 **sans** le multithreading : 1min14.73 égalité
IA vs IA lvl 8 **avec** le multithreading : 1min07.10 avec une victoire (gain de 7 secondes)

Ces benchmarks ont été réalisés avec un processeur IntelCore de 13e génération (i7-13700HX, 16 coeurs)  et une RAM de 32Go.

Le fait que la 2e version ne mène pas à une égalité indique que les IA ne fonctionnent pas exactement de la même manière mais nous n'avons pas trouvé pourquoi. Nous vous mettons tout de même nos essais non concluants dans le fichier ZIP.