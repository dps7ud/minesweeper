"""Minesweeper.py
Class: MsGame - object holding all game related information

TODO: remove all I/O from this file
"""

import itertools
import random
import re


def _pair_range(len_outter, len_inner):
    """Produces all pairs 0..len_outter - 1, 0..len_inner - 1"""
    for ii in range(len_outter):
        for jj in range(len_inner):
            yield ii, jj


class MsGame:
    """Fields:
        board: List of lists holding all apperance information 
                    (flagged squares, cleared squares etc.)
        gameOver: binary indicating if game is over (True) or can be played (False)
        mines: list of tuples indicating positions of mines
        squares: list of tuples of valid board squares 
                    (useful for not picking out of bounds squares)
        before_first_guess: bool indicating if the first guess has been made
    Methods:
        __init__(): populates self.squares and prints initial blank board
        prettyprint(): prints board for user consumption
        getCount(tuple): counts mines touching the square indicated by passed tuple
        lose(): ends game in loss
        isFirst(): Checks if board is fresh (returns True) or not (returns False)
        winCheck(): Checks if user has won game (currently requires all mines to be flagged)
        clear(tuple): Recursive function that attempts to clear square indicated 
                    by passed tuple. Autoclears zeros and ends game if square is mined
        play(Tuple[str,int,int]): handles all other logic for guessing 
            (flagging v. clearing, adjusts gameOver etc.). Tuple contains
            guess type, x and y coords of guess.
        FLAGGED: static value of star (*). Indicates squares that have been flagged.
        DEFAULT: static value of dash (-). Indicates squares that has not been cleared or flagged.
    """

    FLAGGED = '*'
    DEFAULT = '-'
    board = [[ '-' ] * 10 for xx in range(10)]
    game_over = 0
    mines = []
    num_mines = 0
    squares = []
    before_first_guess = True

    def __init__(self, given_mines=None):
        if given_mines is not None:
            self.num_mines = len(list(set(self.mines)))
            self.mines = given_mines
        for ii, jj in _pair_range(10, 10):
            self.squares.append( (ii,jj) )
        self.prettyprint()

    def setup_mines(self, guessed_square):
        if not self.mines:
            self.num_mines = 10
            for ii in range(self.num_mines):
                x = random.randint(0,9)
                y = random.randint(0,9)
                while (x,y) in self.mines or (x,y) == guessed_square:
                    x = random.randint(0,9)
                    y = random.randint(0,9)
                self.mines.append((x,y))
        else:
            return
            

    def prettyprint(self):
        """For printing board to user"""
        print('XX' + "0123456789")
        for ii in range(len(self.board)):
            print(str(ii) + ':',end='')
            for ch in self.board[ii]:
                print(ch,end='')
            print('')
            
    def getCount(self,square):
        """accepts tuple inicating target square
        returns number of neighbours in mines list (counts self)
        """
        lst = []
        l = [-1,0,1]
        for ii, jj in itertools.product(l, repeat=2):
            lst.append((square[0] + ii, square[1] + jj))
        return len(set(lst).intersection(set(self.mines)))

    def lose(self):
        """call to lose game"""
        for mine in self.mines:
            self.board[mine[0]][mine[1]] = 'X'
        self.prettyprint()
        print("Game Over")
        self.game_over = -1

    def isFirst(self):
        """returns true iff called before the first guess
        TODO: repace with bool
        """
        for row in self.board:
            for item in row:
                if item != self.DEFAULT:
                    return False
        return True

    def winCheck(self):
        """return true iff game has been won"""
        dashes = 0
        bangs = 0
        for row in self.board:
            for square in row:
                if square == self.DEFAULT:
                    dashes += 1
                if square == self.FLAGGED:
                    bangs += 1
        return bangs + dashes == self.num_mines

    def clear(self,tup):
        """Clear indicated square. If square holds zero, 
        recursively call on neighbors to find space.
        """
        l = [-1,0,1]
        lst = []
        num = self.getCount(tup)
        self.board[tup[0]][tup[1]] = str(num)
        if num == 0:
            for ii in l:
                for jj in l:
                    lst.append((tup[0] + ii, tup[1] + jj))
            lst = list(set(lst).intersection(set(self.squares)))
            lst.remove(tup)
            for element in lst:
                if self.board[element[0]][element[1]] == self.DEFAULT:
                    self.clear(element)

    def get_board(self):
        """returns board state"""
        return self.board

    def play(self,tup):
        """ Handles guesses of all (flagging, solveing, clearing) types.
        Bad things here:
            Checks if any given guess is the first (bad).
            'tguess' and 'tup' both needed?
            Returns board status on every call
            Is massive and poorly documented
            Performs setup
            Performs checks using 'board' rather than 'flagged'
            Does a lot of I/O
        """
        tguess = (tup[1],tup[2])
        if self.isFirst():
            """Need to call out first guess so that we don't find a mine"""
            if tup[0] != 'c':
                return (self.game_over, board)
            self.setup_mines(tguess)
            self.clear((tup[1],tup[2]))
            self.prettyprint()
            if self.winCheck():
                print("Game over, you win!")
                self.game_over = 1
            return ( (self.game_over, self.board) )
        if not self.game_over:            
            """c -> clearing guess"""
            if tup[0] == 'c':
                if self.board[tguess[0]][tguess[1]] != self.DEFAULT:
                    print("Pick a different square")
                    return (self.game_over, self.board)
                if tguess in self.mines:
                    self.lose()
                    return (self.game_over, self.board)
                #Not a mine so clear it
                self.clear(tguess)                

            elif tup[0] == 'f':
                """f -> flag guess"""
                if self.board[tguess[0]][tguess[1]] == self.FLAGGED:
                    self.board[tguess[0]][tguess[1]] = self.DEFAULT
                    
                elif self.board[tguess[0]][tguess[1]] == self.DEFAULT:
                    self.board[tguess[0]][tguess[1]] = self.FLAGGED
                if self.board[tguess[0]][tguess[1]] not in [self.FLAGGED,self.DEFAULT]:
                    print("Pick a different square")                

            elif tup[0] == 's':
                """s -> solve guess"""
                num = self.board[tguess[0]][tguess[1]]
                if num in ['X',self.FLAGGED,self.DEFAULT]:
                    print("One of X*-")
                    return (self.game_over, self.board)
                adds = [-1,0,1]
                lst = []
                for a in adds:
                    for b in adds:
                        lst.append( (tguess[0] + a, tguess[1] + b) )
                lst.remove(tguess)
                #TODO: list comprehension 
                smines = []
                surround = list(set(self.squares).intersection(set(lst)))
                for s in surround:
                    if self.board[s[0]][s[1]] == self.FLAGGED:
                        smines.append(s)
                if int(num) != len(smines):
                    return (self.game_over,self.board)
                if set(smines).intersection(set(self.mines)) != set(smines):
                    self.lose()
                    return (self.game_over,self.board)
                surround = set(surround).difference(set(self.mines))
                for sq in surround:
                    self.clear(sq)
            self.prettyprint()
            if self.winCheck():
                print("Game over, you win!")
                self.game_over = 1
            return ( (self.game_over, self.board) )
