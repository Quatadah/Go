# GO

## Auteurs:

-   [NASDAMI Quatadah](Quatadah.Nasdami@enseirb-matmeca.fr)
-   [LAMHAMDI Aymane](Aymane.Lamhamdi@enseirb-matmeca.fr)

## Implémentation des algorithmes

Au début, nous avons commencé par implémenter l'algorithme MinMax. Mais comme la taille de l'arbre de recherche est énorme dans le jeu de GO, nous avons fini par implémenter l'algorithme AlphaBeta pour réduire nos recherches et ne pas pedre de temps à parcourir des noeuds inutilement.

## Heuristique

Vu la complexité du jeu de Go, nous n'avons à présent pas trouvé de bonnes heuristiques pour évaluer nos coups. Nous avons donc tenté une évaluation simple en fonction du nombre de pièces, leurs positions sur le plateau de Go, leurs libertés et le nombre des pièces capturées.
Une autre approche a été implémentée pour limiter la profondeur de l'arbre de recherche est celle de Monte Carlo, l'un de ses algorithmes les plus primitifs consiste à choisir les coups aléatoirement, et à évaluer chaque position par la moyenne du résultat de toutes les parties aléaotoires qui passent par cette position.

## Améliorations possibles

Pour l'approche de Monte Carlo, on pourrait ne pas choisir les coups de manière uniformément aléatoire. On peut choisir des coups qui semblent meilleurs a priori pour contrer une menace par exemple.
Nous pourrions aussi prendre des décisions en utilisant le modèle CNN pour évaluer un tableau.

## Joueurs

-   MonteCarloPlayer.py : suit l'algorithme de Monte Carlo.
-   MiniMaxPlayer.py : utilise l'algorithme minimax pour le parcours de l'arbre de recherche.
-   AlphaBetha.py: utilise l'algorithme minimax avec élagage alphabetha
-   myPlayer.py: copie de l'algorithme alphabetha

## EXEMPLES DE LIGNES DE COMMANDES:

-   python3 localGame.py
    --> Va lancer un match myPlayer.py contre myPlayer.py

-   python3 namedGame.py myPlayer.py randomPlayer.py
    --> Va lancer un match entre votre joueur (NOIRS) et le randomPlayer
    (BLANC)

-   python3 namedGame.py gnugoPlayer.py myPlayer.py
    --> gnugo (level 0) contre votre joueur (très dur à battre)
