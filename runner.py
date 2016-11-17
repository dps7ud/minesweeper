""" runner.py
A script to play a number of minesweeper games 
TODO: remove unwanted (nearly all) I/O from this file
      get rid of copy of board (called 'info').
"""

import twoms as ms
import random

game = ms.MsGame()
cleared = []
flagged = []

def clear(tup):
    """Submits clearing guess to game object"""
    if tup in cleared:
        print("Duplicate guess: " + str(tup))
        return
    val = game.play(('c',tup[0],tup[1]))
    cleared.append(tup)
    return val

info = clear((5,5))
board = info[1] 

def flag(tup):
    """Marked the given square as flagged.
    #TODO: Doesn't work for unflagging
    """
    if tup in flagged:
        print("Tuple already flagged")
    val = game.play(('f',tup[0],tup[1]))
    flagged.append(tup)
    return val

def solve(tup):
    """Submits solving guess to game object.
    TODO: oneliner function
    """
    val = game.play(('s', tup[0], tup[1]))
    return val

def getAround(tup):
    """ Returns a list of squares adjacent to the input square."""
    l = [-1,0,1]
    around = []
    for a in l:
        for b in l:
            if 0 > tup[0] + a or 9 < tup[0] + a or 0 > tup[1] + b or 9 < tup[1] + b:
                continue
            around.append( (tup[0] + a, tup[1] + b) ) 
    return around

def retreive(tup, board):
    """find character at tuple"""
    return board[tup[0]][tup[1]]

"""Script
"""
while not info[0]:
    shown = set([])
    for row in board:
        shown = shown.union(set(row))
    if '0' in shown:
        break
    else:
        x = 0
        y = 0
        #TODO: Need all these conditions?
        while ( (x,y) in flagged + cleared ) or ( board[x][y] != '-'):
            x = random.randint(0,9)
            y = random.randint(0,9)
        info = clear((x,y))
lst = [ [] for x in range(8)]
changed = 1
while not info[0]:
    print(changed)
    if not changed:
        print("hung")
        break
    changed = 0
    for ii in range(10):
        for jj in range(10):
            c = retreive((ii,jj), board)
            if c in ['*','-','0']:
                continue
            else:
                n = int(c)
                around = getAround((ii,jj))
                around.remove( (ii,jj) )
                hidden = []
                flagCount = 0
                for a in around:
                    sym = retreive(a,board)
                    if sym == '-':
                        hidden.append(a)
                    elif sym == '*':
                        flagCount += 1
                if len(hidden) + flagCount == n and len(hidden) > 0:
                    for h in hidden:
                        info = flag(h)
                        board = info[1]
                    changed = 2
    for ii in range(10):
        for jj in range(10):
            c = retreive((ii,jj), board)
            if c in ['*','0','-']:
                continue
            n = int(c)
            around = getAround( (ii,jj))
            around.remove( (ii,jj) )
            flagCount = 0
            hiddenCount = 0
            for a in around:
                sym = retreive(a,board)
                if sym == '*':
                    flagCount += 1
                if sym == '-':
                    hiddenCount += 1
            if flagCount == n and hiddenCount != 0:
                if info[0]:
                    break
                info = solve( (ii,jj))
                changed = 3
                board = info[1]
if info[0] == -1:
    print("Lost")
elif info[0] == 1:
    print("Won")
