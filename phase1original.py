#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 16:19:56 2020

@author: theo
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 17:31:00 2020

@author: theo
"""

from typing import List
from lib.gopherpysat import Gophersat
from wumpus import WumpusWorld

N = 4 # Taille de la grille

## Ligne à remplacer avec VOTRE emplacement et nom de l'exécutable gophersat :
## Attention ! Sous Windows, il faut remplacer les '\' par des '/' dans le chemin

gophersat_exec = "/home/theo/go/bin/gophersat"


def creationVoc(n) -> List[str] : #Création des variables pour les 5 éléments du monde (W, S, P, B) pour un monde de taille n*n
    voc = []
    for i in range(n):
        for j in range(n):
            voc.append("W{}_{}".format(i, j))
            voc.append("S{}_{}".format(i, j))
            voc.append("P{}_{}".format(i, j))
            voc.append("B{}_{}".format(i, j))
            voc.append("E{}_{}".format(i, j))
    return voc

def ajoutClausesBreeze(gs, i, j):
    r = ["-B{}_{}".format(i, j)]
    if(i-1 >= 0):
        gs.push_pretty_clause(["B{}_{}".format(i, j), "-P{}_{}".format(i-1, j)])
        r.append("P{}_{}".format(i-1, j))
    if(i+1 < N):
        gs.push_pretty_clause(["B{}_{}".format(i, j), "-P{}_{}".format(i+1, j)])
        r.append("P{}_{}".format(i+1, j))
    if(j-1 >= 0):
        gs.push_pretty_clause(["B{}_{}".format(i, j), "-P{}_{}".format(i, j-1)])
        r.append("P{}_{}".format(i, j-1))
    if(j+1 < N):
        gs.push_pretty_clause(["B{}_{}".format(i, j), "-P{}_{}".format(i, j+1)])
        r.append("P{}_{}".format(i, j+1))
    gs.push_pretty_clause(r)

def ajoutClausesStench(gs, i, j):
    r = ["-S{}_{}".format(i, j)]
    if(i-1 >= 0):
        gs.push_pretty_clause(["S{}_{}".format(i, j), "-W{}_{}".format(i-1, j)])
        r.append("W{}_{}".format(i-1, j))
    if(i+1 < N):
        gs.push_pretty_clause(["S{}_{}".format(i, j), "-W{}_{}".format(i+1, j)])
        r.append("W{}_{}".format(i+1, j))
    if(j-1 >= 0):
        gs.push_pretty_clause(["S{}_{}".format(i, j), "-W{}_{}".format(i, j-1)])
        r.append("W{}_{}".format(i, j-1))
    if(j+1 < N):
        gs.push_pretty_clause(["S{}_{}".format(i, j), "-W{}_{}".format(i, j+1)])
        r.append("W{}_{}".format(i, j+1))
    gs.push_pretty_clause(r)

def ajoutClauseEmpty(gs, i, j):
    gs.push_pretty_clause(["B{}_{}".format(i, j), "S{}_{}".format(i, j), "P{}_{}".format(i, j), "W{}_{}".format(i, j), "E{}_{}".format(i, j)])
    gs.push_pretty_clause(["-E{}_{}".format(i, j), "-B{}_{}".format(i, j)])
    gs.push_pretty_clause(["-E{}_{}".format(i, j), "-S{}_{}".format(i, j)])
    gs.push_pretty_clause(["-E{}_{}".format(i, j), "-P{}_{}".format(i, j)])
    gs.push_pretty_clause(["-E{}_{}".format(i, j), "-W{}_{}".format(i, j)])

def ajoutClausesWumpus(gs, i, j):
    gs.push_pretty_clause(["-P{}_{}".format(i, j), "-W{}_{}".format(i, j)])
    if(i-1 >= 0):
        gs.push_pretty_clause(["-W{}_{}".format(i, j), "S{}_{}".format(i-1, j)])
    if(i+1 < N):
        gs.push_pretty_clause(["-W{}_{}".format(i, j), "S{}_{}".format(i+1, j)])
    if(j-1 >= 0):
        gs.push_pretty_clause(["-W{}_{}".format(i, j), "S{}_{}".format(i, j-1)])
    if(j+1 < N):
        gs.push_pretty_clause(["-W{}_{}".format(i, j), "S{}_{}".format(i, j+1)])
    for a in range(N):
        for b in range(N):
            if(not(a == i and b ==j)):
                gs.push_pretty_clause(["-W{}_{}".format(i, j), "-W{}_{}".format(a, b)])


def ajoutClausesPuit(gs, i, j):
    if(i-1 >= 0):
        gs.push_pretty_clause(["-P{}_{}".format(i, j), "B{}_{}".format(i-1, j)])
    if(i+1 < N):
        gs.push_pretty_clause(["-P{}_{}".format(i, j), "B{}_{}".format(i+1, j)])
    if(j-1 >= 0):
        gs.push_pretty_clause(["-P{}_{}".format(i, j), "B{}_{}".format(i, j-1)])
    if(j+1 < N):
        gs.push_pretty_clause(["-P{}_{}".format(i, j), "B{}_{}".format(i, j+1)])


def isWumpus(gs,i,j):
    gs.push_pretty_clause(["-W{}_{}".format(i, j)])
    isWumpus = not(gs.solve())
    gs.pop_clause()
    return isWumpus

def isStench(gs,i,j):
    gs.push_pretty_clause(["-S{}_{}".format(i, j)])
    isStench = not(gs.solve())
    gs.pop_clause()
    return isStench

def isBreeze(gs,i,j):
    gs.push_pretty_clause(["-B{}_{}".format(i, j)])
    isBreeze = not(gs.solve())
    gs.pop_clause()
    return isBreeze

def isPuit(gs,i,j):
    gs.push_pretty_clause(["-P{}_{}".format(i, j)])
    isPuit = not(gs.solve())
    gs.pop_clause()
    return isPuit

def isEmpty(gs,i,j):
    gs.push_pretty_clause(["-E{}_{}".format(i, j)])
    isEmpty = not(gs.solve())
    gs.pop_clause()
    return isEmpty

def isSafe(gs, i, j):
    gs.push_pretty_clause(["P{}_{}".format(i, j)])
    resPuit = gs.solve()
    gs.pop_clause()
    gs.push_pretty_clause(["W{}_{}".format(i, j)])
    resWumpus = gs.solve()
    gs.pop_clause()
    if((resPuit or resWumpus) == False):
        return True
    else :
        return False

def fullKnowledge(knowledge):
    for k in knowledge:
        if('' in k):
            return False
    return True

def globalProbe(knowledge, gs, ww):
    changement = True
    while(changement):
        changement = False
        for a in range(N):
            for b in range(N):
                if (knowledge[a][b]==''): #on ne connait pas la case
                    # if(isBreeze(gs, a, b)):
                    #     gs.push_pretty_clause(["B{}_{}".format(a, b)])
                    #     knowledge[a][b] += "-"
                    #     changement = True
                    if(isPuit(gs, a, b)):
                        gs.push_pretty_clause(["P{}_{}".format(a, b)])
                        knowledge[a][b] += "P"
                        changement = True
                    # if(isStench(gs, a, b)):
                    #     gs.push_pretty_clause(["S{}_{}".format(a, b)])
                    #     knowledge[a][b] += "-"
                    #     changement = True
                    # if(isEmpty(gs, a, b)):
                    #     gs.push_pretty_clause(["E{}_{}".format(a, b)])
                    #     knowledge[a][b] += "-"
                    #     changement = True
                    if(isWumpus(gs, a, b)):
                        gs.push_pretty_clause(["W{}_{}".format(a, b)])
                        knowledge[a][b] = "W"
                        changement = True
                        
                    if(isSafe(gs, a, b)):
                        changement = True
                        probe1=ww.probe(a, b)
                        knowledge[a][b] = probe1[1]
                        if ('.' in probe1[1]): #la case est empty
                            gs.push_pretty_clause(["E{}_{}".format(a, b)])

                        if ('B' in probe1[1]): #la case est breeze
                            gs.push_pretty_clause(["B{}_{}".format(a, b)])

                        if ('S' in probe1[1]): #la case est stenchy
                            gs.push_pretty_clause(["S{}_{}".format(a, b)])

                # if (knowledge[a][b]=='-'): #on ne connait pas la case
                #     if(isWumpus(gs, a, b)):
                #         gs.push_pretty_clause(["W{}_{}".format(a, b)])
                #         knowledge[a][b] = "W"
                #         changement = True
                #     elif(isPuit(gs, a, b)):
                #         gs.push_pretty_clause(["P{}_{}".format(a, b)])
                #         knowledge[a][b] = "P"
                #         changement = True
    return knowledge


def cautious(knowledge, gs, ww):
    for a in range(N):
        for b in range(N):
            if knowledge[a][b]=='':
                probe1=ww.cautious_probe(a,b)
                knowledge[a][b] = probe1[1]
                if ('.' in probe1[1]): #la case est empty
                    gs.push_pretty_clause(["E{}_{}".format(a, b)])

                if ('B' in probe1[1]): #la case est breeze
                    gs.push_pretty_clause(["B{}_{}".format(a, b)])

                if ('S' in probe1[1]): #la case est stenchy
                    gs.push_pretty_clause(["S{}_{}".format(a, b)])

                if ('W' in probe1[1]): #la case est Wumpus
                    gs.push_pretty_clause(["W{}_{}".format(a, b)])

                if ('P' in probe1[1]): #la case est Puit
                    gs.push_pretty_clause(["P{}_{}".format(a, b)])
                return knowledge

def initialisation(N, random = False):
    ww = WumpusWorld(N, random)
    voc = creationVoc(ww.get_n())
    gs = Gophersat(gophersat_exec, voc)

    #état des lieux 1: on ne sait rien
    knowledge = [[]] * ww.get_n()
    for i in range(ww.get_n()):
        knowledge[i] = [''] * ww.get_n()
        for j in range(ww.get_n()):
            ajoutClauseEmpty(gs, i, j)
            ajoutClausesBreeze(gs, i, j)
            ajoutClausesStench(gs, i, j)
            ajoutClausesWumpus(gs, i, j)
            ajoutClausesPuit(gs, i, j)
    #on probe l'unique case safe
    probe1=ww.probe(0, 0)
    knowledge[0][0] = probe1[1]
    if ('.' in probe1[1]): #la case est empty
        gs.push_pretty_clause(["E0_0"])

    if ('B' in probe1[1]): #la case est breeze
        gs.push_pretty_clause(["B0_0"])

    if ('S' in probe1[1]): #la case est stenchy
        gs.push_pretty_clause(["S0_0"])
    return(ww, gs, knowledge)

def cartographie(ww, gs, knowledge):
    #début du bordel
    while fullKnowledge(knowledge)==False:
        knowledge = globalProbe(knowledge, gs, ww)
        if(fullKnowledge(knowledge)==False):
            knowledge = cautious(knowledge, gs, ww)
    return(ww, gs, knowledge)

def rechercheGold(ww, gs, knowledge):
    for a in range(N):
        for b in range(N):
            if "-" in knowledge[a][b]:
                probe1=ww.probe(a, b)
                knowledge[a][b] = probe1[1]
    return(ww, gs, knowledge)

if __name__ == "__main__":
    (ww, gs, knowledge) = initialisation(N, True)
    (ww, gs, knowledge) = cartographie(ww, gs, knowledge)
    print("toutes les cases ont été sondés! je connais à présent ma géographie!")
    print(knowledge)
    print(ww)
    print(ww.get_cost())
    #(ww, gs, knowledge) = rechercheGold(ww, gs, knowledge)

