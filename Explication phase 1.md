# IA02 Projet Wumpus Phase 1
## Felix Poullet-Pages & Théophane Durand.

### Initialisation

L'initialisation se fait avec la fonction
`initialisation(N, random)`
On lui donne un N pour la taille de la grille et le boolean `random` est pour la création du monde (selon la bibliotheque WumpusWorld)

On créé un monde avec Wumpus World.
On créé le vocabulaire :

#### Vocabulaire :
La fonction creationVoc(n) créé le vocabulaire pour gophersat.

La fonction créé pour chaque case une variable pour la présence ou non su Wumpus, d'un puit, d'un stench, d'un breeze ou de rien du tout.
Il y a donc N² * 5 variables.
#### ---------------

On initialse ensuite  un tableau knowledge pour nous permettre de naviguer dans ce que nous connaissons de la carte.

On ajoute ensuite toutes les différentes rêgles su chaque cases.

#### ajoutClause
Les différents fonction ajoutClause permettent d'implémenter les rêgles du wumpus sur chaque cases.
Par exemple si il y a un puit sur une case alors il y a un breeze sur les cases adjacentes.
#### ---------------

On réalise ensuite un prob sur la premiere case et on ajoute dans gophersat la clause correspondate ainsi que dans notre matrice knowledge.

### Cartographie
Pour cartographier la carte, on vérifie grace à la fonction `fullKnowledge` si il reste des cases inconnues.
Si oui, on réalise la fonction `globalProbe`

#### globalProbe
La fonction `globalProbe` est le coeur de notre programme de cartographie.
Si une case est inconnue, elle teste s'il est certain qu'un puit soit à cette place. Si oui elle créé la clause pour gophersat et entre cette information dans la matrice knowledge.
Elle teste ensuite s'il est certain qu'il y a un wumpus à cette place.
Si oui elle créé la clause pour gophersat et entre cette information dans la matrice.

*On test ensuite s'il est certain qu'il y ait un stench, un breeze ou rien du tout.
Si c'est le cas on ajoute ces informations à la base de connaissance de gophersat et à la matruce knowledge.* **Cependant cette fonctionnalité fait bugger tout le programme on ne comprend pas pourquoi. d'autres puit appariassent à des endroits incohérents**

Si c'est ni l'un ni l'autre elle teste s'il est certain que la case est sure ou non.
Si oui elle effectue un probe sur cette case et entre dans gophersat et dans la matrice knowledge les données correspondantes.

S'il y a eu un changement sur la matrice knowledge (donc des information supplémentaire) on recommence le même processus.
#### -----------------

Si `globalProbe` ne peut plus faire de changement mais qu'il reste des cases inconnues, on effectue la fonction `cautious`

#### cautious
La fonction cautious va chercher la premiere case inconnue et effectue un `cautious_probe` dessus. Elle entre ensuite les données correspondantes dans gophersat et dans la matrice knowledge.
#### -------

Une fois la fonction `cautious`, s'il reste des cases inconnues on recommence avec la fonction `globalProbe` et ainsi de suite.

On vérifie ensuite grace à la fonction `rechercheGold` s'il y a de l'or sur les cases devinées sans `probe` ou `cautious_probe` **Cette fonctionnalité n'est pas activée car inutile tant que le bug de `globalProbe` n'est pas résolu**

lorsque toutes les cases ont été découvertes on affiche la matrice knowledge ainsi que le cout de cartographie.
