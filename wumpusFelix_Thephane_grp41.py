#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lib.wumpus_client import WumpusWorldRemote
from lib.gopherpysat import Gophersat
from requests.exceptions import HTTPError

__author__ = "Théophane Durand"
__copyright__ = "Copyright 2020, UTC"
__license__ = "LGPL-3.0"
__version__ = "0.1.0"
__maintainer__ = "Théophane Durand"
__status__ = "dev"


#size = 5 # Taille de la grille

## Ligne à remplacer avec VOTRE emplacement et nom de l'exécutable gophersat :
## Attention ! Sous Windows, il faut remplacer les '\' par des '/' dans le chemin

gophersat_exec = "/home/theo/go/bin/gophersat"


class Case():
    """A case class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def creationVoc(n): #Création des variables pour les 5 éléments du monde (W, S, P, B) pour un monde de taille n*n
    voc = []
    for i in range(n):
        for j in range(n):
            voc.append("W{}_{}".format(i, j))
            voc.append("S{}_{}".format(i, j))
            voc.append("P{}_{}".format(i, j))
            voc.append("B{}_{}".format(i, j))
            voc.append("E{}_{}".format(i, j))
    return voc

def ajoutClausesBreeze(size, gs, i, j):
    r = ["-B{}_{}".format(i, j)]
    if(i-1 >= 0):
        gs.push_pretty_clause(["B{}_{}".format(i, j), "-P{}_{}".format(i-1, j)])
        r.append("P{}_{}".format(i-1, j))
    if(i+1 < size):
        gs.push_pretty_clause(["B{}_{}".format(i, j), "-P{}_{}".format(i+1, j)])
        r.append("P{}_{}".format(i+1, j))
    if(j-1 >= 0):
        gs.push_pretty_clause(["B{}_{}".format(i, j), "-P{}_{}".format(i, j-1)])
        r.append("P{}_{}".format(i, j-1))
    if(j+1 < size):
        gs.push_pretty_clause(["B{}_{}".format(i, j), "-P{}_{}".format(i, j+1)])
        r.append("P{}_{}".format(i, j+1))
    gs.push_pretty_clause(r)

def ajoutClausesStench(size, gs, i, j):
    r = ["-S{}_{}".format(i, j)]
    if(i-1 >= 0):
        gs.push_pretty_clause(["S{}_{}".format(i, j), "-W{}_{}".format(i-1, j)])
        r.append("W{}_{}".format(i-1, j))
    if(i+1 < size):
        gs.push_pretty_clause(["S{}_{}".format(i, j), "-W{}_{}".format(i+1, j)])
        r.append("W{}_{}".format(i+1, j))
    if(j-1 >= 0):
        gs.push_pretty_clause(["S{}_{}".format(i, j), "-W{}_{}".format(i, j-1)])
        r.append("W{}_{}".format(i, j-1))
    if(j+1 < size):
        gs.push_pretty_clause(["S{}_{}".format(i, j), "-W{}_{}".format(i, j+1)])
        r.append("W{}_{}".format(i, j+1))
    gs.push_pretty_clause(r)

def ajoutClauseEmpty(gs, i, j):
    gs.push_pretty_clause(["B{}_{}".format(i, j), "S{}_{}".format(i, j), "P{}_{}".format(i, j), "W{}_{}".format(i, j), "E{}_{}".format(i, j)])
    gs.push_pretty_clause(["-E{}_{}".format(i, j), "-B{}_{}".format(i, j)])
    gs.push_pretty_clause(["-E{}_{}".format(i, j), "-S{}_{}".format(i, j)])
    gs.push_pretty_clause(["-E{}_{}".format(i, j), "-P{}_{}".format(i, j)])
    gs.push_pretty_clause(["-E{}_{}".format(i, j), "-W{}_{}".format(i, j)])

def ajoutClausesWumpus(size, gs, i, j):
    gs.push_pretty_clause(["-P{}_{}".format(i, j), "-W{}_{}".format(i, j)])
    if(i-1 >= 0):
        gs.push_pretty_clause(["-W{}_{}".format(i, j), "S{}_{}".format(i-1, j)])
    if(i+1 < size):
        gs.push_pretty_clause(["-W{}_{}".format(i, j), "S{}_{}".format(i+1, j)])
    if(j-1 >= 0):
        gs.push_pretty_clause(["-W{}_{}".format(i, j), "S{}_{}".format(i, j-1)])
    if(j+1 < size):
        gs.push_pretty_clause(["-W{}_{}".format(i, j), "S{}_{}".format(i, j+1)])
    for a in range(size):
        for b in range(size):
            if(not(a == i and b ==j)):
                gs.push_pretty_clause(["-W{}_{}".format(i, j), "-W{}_{}".format(a, b)])


def ajoutClausesPuit(size, gs, i, j):
    if(i-1 >= 0):
        gs.push_pretty_clause(["-P{}_{}".format(i, j), "B{}_{}".format(i-1, j)])
    if(i+1 < size):
        gs.push_pretty_clause(["-P{}_{}".format(i, j), "B{}_{}".format(i+1, j)])
    if(j-1 >= 0):
        gs.push_pretty_clause(["-P{}_{}".format(i, j), "B{}_{}".format(i, j-1)])
    if(j+1 < size):
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

def globalProbe(size, knowledge, gs, wwr):
    changement = True
    while(changement):
        changement = False
        for a in range(size):
            for b in range(size):
                if (knowledge[a][b]==''): #on ne connait pas la case
                    # if(isBreeze(gs, a, b)):
                    #     gs.push_pretty_clause(["B{}_{}".format(a, b)])
                    #     knowledge[a][b] += "-"
                    #     changement = True
                    if(isPuit(gs, a, b)):
                        gs.push_pretty_clause(["P{}_{}".format(a, b)])
                        knowledge[a][b] += "P"
                        wwr.know_pit(a, b)
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
                        wwr.know_wumpus(a, b)
                        changement = True
                        
                    if(isSafe(gs, a, b)):
                        changement = True
                        probe1=wwr.probe(a, b)
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
    #return knowledge


def cautious(size, knowledge, gs, wwr):
    for a in range(size):
        for b in range(size):
            if knowledge[a][b]=='':
                probe1=wwr.cautious_probe(a,b)
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
                #return knowledge

def initialisation(size, wwr):
    #ww = WumpusWorld(size, random)
    voc = creationVoc(size)
    gs = Gophersat(gophersat_exec, voc)

    #état des lieux 1: on ne sait rien
    knowledge = [[]] * size
    for i in range(size):
        knowledge[i] = [''] * size
        for j in range(size):
            ajoutClauseEmpty(gs, i, j)
            ajoutClausesBreeze(size, gs, i, j)
            ajoutClausesStench(size, gs, i, j)
            ajoutClausesWumpus(size, gs, i, j)
            ajoutClausesPuit(size, gs, i, j)
    #on probe l'unique case safe
    status, probe1, cost=wwr.probe(0, 0)
    knowledge[0][0] = probe1
    if ('.' in probe1): #la case est empty
        gs.push_pretty_clause(["E0_0"])

    if ('B' in probe1): #la case est breeze
        gs.push_pretty_clause(["B0_0"])

    if ('S' in probe1): #la case est stenchy
        gs.push_pretty_clause(["S0_0"])
    return(gs, knowledge)

def cartographie(size, wwr, gs, knowledge):
    #début du bordel
    while fullKnowledge(knowledge)==False:
        globalProbe(size, knowledge, gs, wwr)
        if(fullKnowledge(knowledge)==False):
            cautious(size, knowledge, gs, wwr)

def rechercheGold(size, ww, gs, knowledge):
    for a in range(size):
        for b in range(size):
            if "-" in knowledge[a][b]:
                probe1=ww.probe(a, b)
                knowledge[a][b] = probe1[1]
    return(ww, gs, knowledge)


def astar(maze, start, end):

    # Create Case and end case
    start_case = Case(None, start)
    start_case.g = start_case.h = start_case.f = 0
    end_case = Case(None, end)
    end_case.g = end_case.h = end_case.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start case
    open_list.append(start_case)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current case
        current_case = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_case.f:
                current_case = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_case)

        # Found the goal
        if current_case == end_case:
            path = []
            current = current_case
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares

            # Get case position
            case_position = (current_case.position[0] + new_position[0], current_case.position[1] + new_position[1])

            # Make sure within range
            if case_position[0] > (len(maze) - 1) or case_position[0] < 0 or case_position[1] > (len(maze[len(maze)-1]) -1) or case_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[case_position[0]][case_position[1]] != 0:
                continue

            # Create new case
            new_case = Case(current_case, case_position)

            # Append
            children.append(new_case)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_case.g + 1
            child.h = ((child.position[0] - end_case.position[0]) ** 2) + ((child.position[1] - end_case.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_case in open_list:
                if child == open_case and child.g > open_case.g:
                    continue

            # Add the child to the open list
            open_list.append(child)

def sucesseurs(size, knowledge, x, y):
    sucesseurs = []
    if(x-1 >= 0):
        if(not('P' in knowledge[x-1][y]) and not('W' in knowledge[x-1][y])):
            sucesseurs.append((x-1, y))
    if(x+1 < size):
        if(not('P' in knowledge[x+1][y]) and not('W' in knowledge[x+1][y])):
            sucesseurs.append((x+1, y))
    if(y-1 >= 0):
        if(not('P' in knowledge[x][y-1]) and not('W' in knowledge[x][y-1])):
            sucesseurs.append((x, y-1))
    if(y+1 < size):
        if(not('P' in knowledge[x][y+1]) and not('W' in knowledge[x][y+1])):
            sucesseurs.append((x, y+1))
    return sucesseurs

def largeur(size, knowledge, suc):
    e = 0
    while e < len(suc):
        for b in sucesseurs(size, knowledge, suc[e][0], suc[e][1]):
            if not(b in suc):
                suc.append(b)
        e+=1

def cestpartit():
        
    # Connexion au server
    server = "http://localhost:8080"
    groupe_id = "Binôme de projet 41"  # votre vrai numéro de groupe
    names = "Théophane Durand et Félix Poullet-pages"  # vos prénoms et noms

    try:
        wwr = WumpusWorldRemote(server, groupe_id, names)
    except HTTPError as e:
        print(e)
        print("Try to close the server (Ctrl-C in terminal) and restart it")
        return
    
    status, msg, size = wwr.next_maze()
    
    nbMaze = 0
    
    while status == "[OK]":
    
        ###################
        ##### PHASE 1 #####
        ###################
        
        (gs, knowledge) = initialisation(size, wwr)
        cartographie(size, wwr, gs, knowledge)
        phase, pos = wwr.get_status()
    
        # La carte doit être entièrement parcourue avant de passer à la phase 2!
        status, msg = wwr.end_map()
        #print(status, msg)
    
        phase, pos = wwr.get_status()
        
        i, j = wwr.get_position()
        ###################
        ##### PHASE 2 #####
        ###################
        
        suc = [(0, 0)]
        largeur(size, knowledge, suc)
        
        terrain = [[1] * size for i in range(size)]
        for a, b in suc:
            terrain[a][b] = 0
        
        goldATrouver = []
        for a in range(size):
            for b in range(size):
                if('G' in knowledge[a][b] and ((a, b) in suc)):
                    goldATrouver.append((a, b))
        #goldATrouver.append((0, 0))       
        
        cheminTotal = []
        pos = wwr.get_position()
        
        for a, b in goldATrouver:
            #print("({}, {})".format(a, b))
            chemin = astar(terrain, pos, (a,b))
            pos = (a, b)
            for case in chemin[1:]:
                cheminTotal.append(case)
                if (case in goldATrouver):
                    goldATrouver.remove(case)
        
        chemin = astar(terrain, pos, (0,0))
        for case in chemin[1:]:
            cheminTotal.append(case)
        
        #print(cheminTotal)
        for i, j in cheminTotal:
            res = wwr.go_to(i, j)
            #print(res)
        res = wwr.maze_completed()
        #print(res)
    
        phase, pos = wwr.get_status()
        
        nbMaze += 1
        print("{} Wumpus terminés".format(nbMaze))
        #input()
        
        
        status, msg, size = wwr.next_maze()
    

if __name__ == "__main__":

    cestpartit()
