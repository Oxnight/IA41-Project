# Teeko - Jeu à Deux Adversaires

## Description
**Teeko** est un jeu de stratégie à deux joueurs où le but est de placer et déplacer ses pions sur un plateau de 5x5 pour former un alignement (horizontal, vertical ou en diagonale) ou un carré de 4 pions.

### Matériel
- **Plateau** : Carré de 5x5 intersections.
- **Pions** : Chaque joueur dispose de 4 pions, l'un noir et l'autre blanc.

## But du Jeu
Le but du jeu est de former, avec ses pions, l'une des configurations gagnantes suivantes :
- Un alignement de 4 pions (horizontal, vertical ou en diagonale).
- Un carré de 4 pions (les coins d'un carré de 2x2).

La partie se déroule en deux phases :
1. **Phase de pose** : Les joueurs placent leurs pions à tour de rôle sur le plateau.
2. **Phase de déplacement** : Après avoir placé tous leurs pions, les joueurs déplacent un de leurs pions à chaque tour sur un emplacement adjacent libre.

La partie se termine dès qu'un joueur parvient à obtenir une configuration gagnante.

## Règles du Jeu
1. **Phase de pose** :
   - Le plateau est vide au départ.
   - Les joueurs placent leurs pions, un à la fois, sur une intersection libre (de 1 à 25, sur le plateau).
   - Un emplacement est libre si aucun pion n'y est déjà présent.

2. **Phase de déplacement** :
   - Après la phase de pose, les joueurs déplacent à tour de rôle un de leurs pions.
   - Un pion ne peut être déplacé que sur un emplacement libre adjacent (horizontale, verticale ou diagonale).
   - Le jeu continue jusqu'à ce qu'un joueur obtienne une configuration gagnante.

## Objectif du Projet
L'objectif est de programmer l'IA (Intelligence Artificielle) d'un ou des deux joueurs. La difficulté de l'IA pourra être ajustée avant le début de la partie. L'IA devra être capable de prendre des décisions stratégiques dans les deux phases du jeu (pose et déplacement).
