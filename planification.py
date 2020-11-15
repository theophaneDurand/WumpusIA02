#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 16:35:36 2020

@author: theo
"""


from wumpus import WumpusWorld
from phase1 import *
from lib.gopherpysat import Gophersat

N = 5 # Taille de la grille 

gophersat_exec = "/home/theo/go/bin/gophersat"

def sucesseurs(knowledge, x, y):
    sucesseurs = []
    if(x-1 >= 0):
        if(not('P' in knowledge[x-1][y]) and not('W' in knowledge[x-1][y])):
            sucesseurs.append((x-1, y))
    if(x+1 < N):
        if(not('P' in knowledge[x+1][y]) and not('W' in knowledge[x+1][y])):
            sucesseurs.append((x+1, y))
    if(y-1 >= 0):
        if(not('P' in knowledge[x][y-1]) and not('W' in knowledge[x][y-1])):
            sucesseurs.append((x, y-1))
    if(y+1 < N):
        if(not('P' in knowledge[x][y+1]) and not('W' in knowledge[x][y+1])):
            sucesseurs.append((x, y+1))
    return sucesseurs

def largeur(knowledge, suc):
    e = 0
    while e < len(suc):
        for b in sucesseurs(knowledge, suc[e][0], suc[e][1]):
            if not(b in suc):
                suc.append(b)
        e+=1

def heuristique(knowledge, a, b):
    heuri = [[0] * N for i in range(N)]
    for x in range(N):
        for y in range(N):
            heuri[x][y] = abs(a-x)+abs(b-y)
    return heuri

        
if __name__ == "__main__":
    (ww, gs, knowledge) = initialisation(N, True)
    (ww, gs, knowledge) = cartographie(ww, gs, knowledge)
    a = sucesseurs(knowledge, 0, 0)
