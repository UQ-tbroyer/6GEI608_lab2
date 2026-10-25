**Thomas BISSONNETTE-ROYER** (BIST15100300)  
**Émeric RENAUD** (RENE05030000)

# Laboratoire #2

**6GEI608 — Intelligence artificielle et reconnaissance des formes**

Travail présenté à  
M. Oussama Jebbar et M. Mikael Brassard

Département des sciences appliquées  
Université du Québec à Chicoutimi

25 octobre 2026

---

## Algorithme A*

Lien de la branche A* : <https://github.com/UQ-tbroyer/6GEI608_lab1/blob/Astar/main.py>

Pour le problème du 8-puzzle, il s’agit de replacer les huit tuiles de la grille 3x3 en déplaçant la case vide jusqu’à obtenir l’état final `1 2 3 / 4 5 6 / 7 8 _`. Contrairement aux algorithmes de recherche du premier laboratoire, A* utilise une heuristique pour choisir le prochain état à explorer. À chaque itération, on prend l’état de la frontière qui a la plus petite valeur *f(n) = g(n) + h(n)*, où *g(n)* est le nombre de déplacements faits depuis le départ et *h(n)* est l’estimation du nombre de déplacements qu’il reste à faire. Aussi, un état déjà exploré n’est pas exploré une deuxième fois et on ajoute un état à la frontière seulement si on l’atteint par un chemin plus court que celui qu’on connaissait déjà.

Pour l’estimation *h(n)*, on a utilisé deux heuristiques :

- **Distance de Manhattan** : pour chaque tuile (sauf la case vide), on additionne le nombre de lignes et de colonnes qui la séparent de sa position finale.
- **Nombre de tuiles mal placées** : on compte le nombre de tuiles (sauf la case vide) qui ne sont pas à la bonne position.

Les deux heuristiques ne surestiment jamais le nombre de déplacements restants, elles sont donc admissibles et A* trouve toujours la solution optimale. Toutefois, la distance de Manhattan donne toujours une valeur plus grande ou égale au nombre de tuiles mal placées, elle est donc plus informée.

Le tableau ci-dessous présente les performances moyennes de A* pour les deux heuristiques sur les 4 puzzles (10 exécutions par puzzle). Par soucis de clarté, on considère 1 itération comme l’exploration d’un état.

| Puzzle | Heuristique | Déplacements de la solution | Nombre d’itérations (états explorés) | Temps moyen |
| --- | --- | --- | ---: | ---: |
| Ex1-1 | Manhattan | 20 | 283 | 7,9 ms |
|  | Tuiles mal placées | 20 | 3 667 | 100,4 ms |
| Ex1-2 | Manhattan | 17 | 233 | 6,3 ms |
|  | Tuiles mal placées | 17 | 984 | 27,0 ms |
| Ex1-3 | Manhattan | aucune solution | 181 440 | 6,97 s |
|  | Tuiles mal placées | aucune solution | 181 440 | 9,88 s |
| Ex1-4 | Manhattan | 28 | 727 | 18,4 ms |
|  | Tuiles mal placées | 28 | 68 754 | 2,24 s |
| **Moyenne (puzzles solubles)** | Manhattan |  | 414 | 10,9 ms |
|  | Tuiles mal placées |  | 24 468 | 790,5 ms |

La première chose que l’on peut observer, c’est que les deux heuristiques trouvent exactement le même chemin, ce qui est normal puisqu’elles sont admissibles. Par contre, la distance de Manhattan explore beaucoup moins d’états, soit 4 fois moins pour Ex1-2, 13 fois moins pour Ex1-1 et 95 fois moins pour Ex1-4. Plus la solution est longue, plus l’écart est grand et le temps d’exécution suit la même tendance. On voit donc qu’une heuristique plus informée guide mieux la recherche.

Pour Ex1-3, aucune des deux heuristiques ne trouve de solution, car ce puzzle n’est pas soluble (son état initial a 27 inversions, ce qui est un nombre impair). A* explore alors 181 440 états, soit 9!/2, ce qui correspond à toute la moitié de l’espace d’états qu’on peut atteindre à partir de ce départ. Comme il faut tout parcourir, les deux heuristiques explorent exactement les mêmes états. Aussi, le nombre d’itérations ne change pas d’un essai à l’autre puisque l’algorithme est déterministe, seul le temps d’exécution varie.

## Problème d’optimisation

Pour le problème, il s’agit tout simplement de remplir une grille de sudoku 9x9 en ayant une solution conforme.

Afin de s’assurer des performances des deux algorithmes, 10 grilles de sudoku seront utilisées. Toutes ces grilles ont été générées par le site web « qqwing.com ». Pour l’échantillon test, quatre seront de difficulté « simple », trois de difficulté « easy » et trois de difficulté « intermediate ».

### Hill climbing

L’heuristique qui a été choisie pour l’algorithme de Hill climbing est le nombre d’erreurs dans la grille, calculé pour la position actuelle et pour chacun de ses voisins. On considère comme erreur tout nombre qui se retrouve en double dans une colonne, une ligne ou son carré 3x3. On cherche donc à minimiser cette fonction heuristique. Bien entendu, les états qui ne gardent pas les nombres de départ aux mêmes endroits sont ignorés et ne sont pas considérés comme des voisins.

Aussi, pour accélérer la recherche, lorsque la grille est remplie aléatoirement au début de la recherche ou lors d’un redémarrage (en cas de minimum local), on remplit chaque **ligne** avec les chiffres de 1 à 9 qui n’y sont pas déjà, placés de façon aléatoire dans les cases vides. Il n’y a ainsi aucune répétition dans une même ligne, et les chiffres déjà présents dans le problème de départ restent à leur place. Un voisin est obtenu en échangeant deux cases vides d’une même ligne.

Pour éviter que la recherche s’arrête trop vite, on accepte aussi les mouvements latéraux, c’est-à-dire les voisins qui ont le même nombre d’erreurs que l’état actuel. Lorsque plusieurs voisins sont aussi bons, on en choisit un au hasard pour ne pas faire le même échange (et son inverse) en boucle. Si aucun voisin n’est meilleur ou égal, ou après 100 mouvements latéraux de suite sans amélioration, on considère qu’on est dans un minimum local et on redémarre avec une nouvelle grille aléatoire. Les redémarrages sont exécutés en parallèle sur tous les cœurs du processeur. Dans le tableau ci-dessous, on analyse les performances de l’algorithme de Hill climbing. Par soucis de clarté, on considère 1 itération comme un redémarrage, c’est-à-dire une montée complète à partir d’une grille aléatoire jusqu’à un minimum local ou jusqu’à la solution.

| Algorithme | Difficulté | Numéro | Temps d’exécution (s) | Nombre d’itérations |
| --- | --- | ---: | ---: | ---: |
| Hill climbing | Simple | 1 | 88,4 | 1 723 |
|  | Simple | 2 | 219,4 | 4 440 |
|  | Simple | 3 | 95,5 | 1 602 |
|  | Simple | 4 | 271,8 | 5 047 |
|  | Easy | 5 | 341,6 | 6 441 |
|  | Easy | 6 | 17,8 | 99 |
|  | Easy | 7 | 128,1 | 2 400 |
|  | Intermediate | 8 | 35,1 | 457 |
|  | Intermediate | 9 | 17,4 | 124 |
|  | Intermediate | 10 | 50,6 | 876 |
|  |  | **Moyenne** | **126,6** | **2 321** |

La première chose que l’on peut observer avec cet échantillon de 10 résolutions, c’est que la vitesse de résolution est assez aléatoire, soit de 17 secondes pour le puzzle 9 à presque 6 minutes pour le puzzle 5. Cela provient de la nature aléatoire des états initiaux et des états de redémarrage. Aussi, la difficulté de qqwing ne semble pas avoir beaucoup d’impact, puisque ce sont les puzzles « intermediate » qui ont été résolus le plus rapidement (34 secondes en moyenne). Il faut aussi noter qu’une première version de l’algorithme, qui n’acceptait pas les mouvements latéraux, prenait en moyenne 2,82 h par puzzle (jusqu’à 12 h pour le puzzle 10). Le simple fait de permettre à l’algorithme de se déplacer sur les plateaux a donc réduit le temps moyen à environ 2 minutes.

### Algorithme génétique

- **Représentation d’un individu** : chaque individu est une grille 9x9 complète. Les chiffres du problème de départ restent à leur place et on remplit les cases vides de chaque ligne avec les chiffres qui manquent, dans un ordre aléatoire. Chaque ligne contient donc toujours les chiffres de 1 à 9 (encodage par permutation). De cette façon, l’algorithme n’a qu’à corriger les erreurs dans les colonnes et les carrés 3x3.
- **Fonction de fitness** : comme pour le Hill climbing, on compte le nombre d’erreurs dans la grille, c’est-à-dire les nombres en double dans les colonnes et les carrés 3x3. On cherche à minimiser cette valeur et une fitness de 0 correspond à une solution.
- **Sélection des parents** : on utilise une sélection par tournoi de taille 3. On choisit trois individus au hasard dans la population et le meilleur des trois devient un parent. Les meilleurs individus ont donc plus de chances d’être choisis, mais les individus moins bons peuvent quand même se reproduire, ce qui garde de la diversité dans la population.
- **Croisement (crossover)** : on fait un croisement par ligne avec une probabilité de 0,9. Pour chaque ligne de l’enfant, on copie la ligne complète du parent 1 ou du parent 2 (une chance sur deux). Comme les lignes sont copiées au complet, elles restent valides.
- **Mutation** : pour chaque ligne de l’enfant, il y a une probabilité de 0,15 d’échanger deux cases vides choisies au hasard. La ligne garde donc les mêmes chiffres, seulement dans un ordre différent.
- **Élitisme** : les 2 meilleurs individus d’une génération sont gardés tels quels pour la génération suivante.
- **Redémarrage** : si la meilleure fitness ne s’améliore pas pendant 60 générations, on considère que la population est coincée dans un minimum local et on la remplace au complet par une nouvelle population aléatoire.
- **Paramètres** : la population contient 150 individus et l’algorithme s’arrête dès qu’un individu a une fitness de 0. Par soucis de clarté, on considère 1 itération comme une génération.

| Algorithme | Difficulté | Numéro | Temps d’exécution (s) | Nombre d’itérations |
| --- | --- | ---: | ---: | ---: |
| Génétique | Simple | 1 | 876,3 | 81 232 |
|  | Simple | 2 | 3 424,3 | 411 135 |
|  | Simple | 3 | 2 034,4 | 662 174 |
|  | Simple | 4 | 2 901,2 | 911 187 |
|  | Easy | 5 | 123,7 | 40 056 |
|  | Easy | 6 | 24,4 | 7 933 |
|  | Easy | 7 | 542,6 | 163 053 |
|  | Intermediate | 8 | 578,3 | 74 992 |
|  | Intermediate | 9 | 432,0 | 136 166 |
|  | Intermediate | 10 | 117,2 | 37 097 |
|  |  | **Moyenne** | **1 105,4** | **252 503** |

#### Analyse de données et discussion du temps d’exécution

Comme pour le Hill climbing, on remarque que le temps de résolution varie beaucoup d’un puzzle à l’autre, soit de 24 secondes pour le puzzle 6 à presque une heure pour le puzzle 2. Cela provient surtout des redémarrages. En regardant les fichiers d’évaluation, on voit que la meilleure fitness descend d’environ 35 erreurs jusqu’à 2 ou 4, reste bloquée, puis remonte lorsque la population est remplacée. Chaque population a donc peu de chances de trouver la solution et le nombre de générations dépend surtout du nombre de redémarrages qu’il a fallu faire. Aussi, puisqu’on fait une seule exécution par puzzle, une partie des écarts est due au hasard.

Contrairement à ce qu’on pourrait penser, la difficulté donnée par qqwing ne permet pas de prédire les résultats de l’algorithme génétique. En effet, ce sont les puzzles « simple » qui ont pris le plus de générations (516 432 en moyenne), alors que les « intermediate » (82 752) et les « easy » (70 347) ont été plus rapides. Cela s’explique par le fait que la difficulté de qqwing est basée sur les techniques qu’un humain doit utiliser pour résoudre la grille, alors que l’algorithme génétique ne fait aucune déduction. Il dépend plutôt du nombre de cases vides, qui est presque le même pour les 10 puzzles (entre 25 et 28 chiffres de départ).

Il faut aussi noter que pour les puzzles 1, 2 et 8, le temps par génération est environ 3 fois plus long que pour les autres puzzles (environ 3,1 ms). Leur temps d’exécution a donc été augmenté par l’ordinateur pendant l’exécution et non par l’algorithme. Pour comparer les puzzles entre eux, le nombre de générations est donc plus fiable que le temps.

#### Comparaison des algorithmes

|  | Hill climbing | Génétique |
| --- | ---: | ---: |
| Temps moyen | 126,6 s | 1 105,4 s |
| Temps moyen, Simple | 168,8 s | 2 309,1 s |
| Temps moyen, Easy | 162,5 s | 230,2 s |
| Temps moyen, Intermediate | 34,4 s | 375,8 s |
| Puzzle le plus rapide | 17,4 s (n° 9) | 24,4 s (n° 6) |
| Puzzle le plus long | 341,6 s (n° 5) | 3 424,3 s (n° 2) |

Les deux algorithmes ont réussi à résoudre les 10 puzzles, mais le Hill climbing a été environ 9 fois plus rapide en moyenne (127 secondes contre 1 105 secondes). Il a été plus rapide pour 9 puzzles sur 10, le puzzle 5 étant la seule exception. Bien entendu, cette comparaison n’est pas tout à fait équitable, puisque le Hill climbing est exécuté en parallèle sur tous les cœurs du processeur alors que l’algorithme génétique utilise un seul cœur. Aussi, on ne peut pas comparer directement le nombre d’itérations, puisqu’une itération du Hill climbing est une montée complète alors qu’une génération de l’algorithme génétique évalue 150 individus.

Avec les mouvements latéraux, chaque montée du Hill climbing peut traverser les plateaux au lieu de s’arrêter au premier, ce qui augmente beaucoup ses chances d’atteindre la solution. Comme une montée est assez rapide et que plusieurs montées sont faites en même temps, l’algorithme essaie un grand nombre de grilles de départ en peu de temps. De son côté, l’algorithme génétique fait évoluer 150 grilles en même temps et peut combiner de bonnes lignes qui viennent de deux grilles différentes grâce au croisement, mais sa population finit souvent par se coincer dans un minimum local, ce qui le force à redémarrer. Toutefois, les deux algorithmes restent sensibles aux minimums locaux et leurs temps de résolution varient beaucoup d’un puzzle à l’autre.

## Ce que nous avons appris

Dans le cadre de ce laboratoire, nous avons appris comment implémenter un nouvel algorithme pour la recherche de solution pour le 8 puzzle soit l’algorithme A* et nous avons également appliqué des concepts d’optimisation à un problème plus complexe soit la résolution de sudoku. Pour ce dernier, les algorithmes de Hill climbing et de génétique ont pu être implémentés.

Pour A*, nous avons pu constater que le choix de l’heuristique est très important. Les deux heuristiques testées donnent toujours la solution optimale, mais la distance de Manhattan explore jusqu’à 95 fois moins d’états que le nombre de tuiles mal placées. Comparé aux algorithmes du premier laboratoire, A* trouve le chemin le plus court en explorant beaucoup moins d’états. Le puzzle Ex1-3 nous a aussi montré qu’il peut être long de conclure qu’un puzzle n’a pas de solution, alors qu’un simple calcul du nombre d’inversions permet de le savoir dès le départ.

Pour le Hill climbing, nous avons pu constater que la simplicité de cet algorithme a un coût : l’algorithme se coince souvent sur des plateaux ou des minimums locaux, ce qui nous force à ajouter un redémarrage à la recherche. Notre première version, qui s’arrêtait dès qu’aucun voisin n’était meilleur, prenait en moyenne près de 3 heures par puzzle. En acceptant les mouvements latéraux, le temps moyen est descendu à environ 2 minutes. De plus, la génération aléatoire de grille qui s’assure qu’il n’y a pas de duplication dans les lignes et l’ajout de parallélisme ont aussi beaucoup aidé à accélérer la recherche.

Pour l’algorithme génétique, nous avons appris que la façon de représenter un individu est aussi importante que les opérateurs. Le fait que chaque ligne contienne toujours les chiffres de 1 à 9 élimine dès le départ une grande partie des grilles invalides, à condition que le croisement et la mutation gardent cette propriété. Nous avons aussi remarqué que la population finit par se coincer dans un minimum local et que c’est le redémarrage après plusieurs générations sans amélioration qui permet de trouver la solution. Finalement, comme pour le Hill climbing, le temps de résolution varie beaucoup d’une exécution à l’autre, c’est pourquoi il est important de comparer les algorithmes sur plusieurs puzzles.