# -*- coding: utf-8 -*-
''' This is the file you have to modify for the tournament. Your default AI player must be called by this module, in the
myPlayer class.

Right now, this class contains the copy of the randomPlayer. But you have to change this!
'''

from time import time

from chess import _BoardState
from sklearn.utils import shuffle
import Goban 
from random import choice
from numpy.random import normal
from playerInterface import *

class myPlayer(PlayerInterface):
    ''' Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of moves given by legal_moves() and used by push() and 
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    '''
    def setBoardScores(self):
        return [
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 2, 2, 2, 1, 2, 2, 2, 0,
            0, 2, 2, 2, 1, 2, 2, 2, 0,
            0, 2, 2, 1, 1, 1, 2, 2, 0,
            0, 1, 1, 1, 1, 1, 1, 1, 0,
            0, 2, 2, 1, 1, 1, 2, 2, 0,
            0, 2, 2, 2, 1, 2, 2, 2, 0,
            0, 2, 2, 2, 1, 2, 2, 2, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0
        ]
        

    def __init__(self):
        self.boardSize = Goban.Board._BOARDSIZE
        self._board = Goban.Board()
        self.scores = self.setBoardScores()

        self._mycolor = None
        self.timeOut = 4
        self.begin = 0
        
    def getPlayerName(self):
        return "IAMANIA"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS" 
        #moves = self._board.legal_moves() # Dont use weak_legal_moves() here!
        #move = choice(moves) 
        move = self.choose_action()
        self._board.push(move)

        # New here: allows to consider internal representations of moves
        print("I am playing ", self._board.move_to_str(move))
        print("My current board :")
        self._board.prettyPrint()
        # move is an internal representation. To communicate with the interface I need to change if to a string
        return Goban.Board.flat_to_name(move) 

    def playOpponentMove(self, move):
        print("Opponent played ", move) # New here
        # the board needs an internal represetation to push the move.  Not a string
        self._board.push(Goban.Board.name_to_flat(move)) 

    def newGame(self, color):
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")

    
    def choose_action(self):
        depth = 1   
        self.begin = time()
        (eval_score, selected_action) = (-1, -1)
        while(True):
            tmp_time = time()
            self.transposition_table = {}
            #new_score, new_action = self.alphabeta(depth, True, float('-inf'), float('+inf'))
            new_score, new_action = self.minimax(depth, True)
            if (time()-self.begin < self.timeOut):
                (eval_score, selected_action) = (new_score, new_action)
            print("MINIMAX AB ID(%d) : eval=%f, action=%d, time=%s" % (depth, eval_score, selected_action, time()-tmp_time))
            if (time()-self.begin >= self.timeOut):
                break
            depth+=1
        return selected_action


    """
    def alphabeta(self, depth, player, alpha, betha):
        now = time()
        if depth == 0 or (now - self.begin >= self.timeOut) or self._board.is_game_over():
            result = (self.eval(), None)    
            return result
        legalMoves = [self._board.generate_legal_moves()]
        shuffle(legalMoves)        
        bestMove= -1
        moveTargets = []        
        if player:            
            bestValue = -999999
            for move in legalMoves:
                self._board.push(move)
                result = self.alphabeta(depth - 1, not player, alpha, betha)
                value, move = max(result[0], value), result[1]                
                self._board.pop()
                if value >= betha:
                    break
                alpha = max(alpha, value)            
            return (value, move)
        else:
            bestValue = 999999
            for move in legalMoves:
                self._board.push(move)
                result = self.alphabeta(depth - 1, not player, alpha, betha)
                value, move = min(result[0], value), result[1]
                self._board.pop()
                if value <= alpha:
                    break
                betha = min(betha, value)
            return (value, move)
    """

    def minimax(self, depth, player):
        now = time()
        if depth == 0 or (now - self.begin >= self.timeOut) or self._board.is_game_over():            
            return (self.eval(), None)
        legalMoves = list(self._board.generate_legal_moves())
        shuffle(legalMoves)                
        if player:            
            bestMoves = []
            bestValue = -999999
            for move in legalMoves:
                self._board.push(move)
                value = self.minimax(depth - 1, not player)[0]
                self._board.pop()
                if (value > bestValue):
                    bestValue = value            
                    bestMoves.append(move)
                elif value == bestValue:
                    bestMoves.append(move)
            return (bestValue, choice(bestMoves))
        else:
            bestMoves = []
            bestValue = 999999
            for move in legalMoves:
                self._board.push(move)                
                value = self.minimax(depth - 1, not player)[0]
                self._board.pop()
                if (value < bestValue):
                    bestValue = value     
                    bestMoves.append(move)    
                elif value == bestValue:
                    bestMoves.append(move)                                  
            return (bestValue, choice(bestMoves))

    def eval(self):       
        pieceScore = 0
        if self._board.next_player() == self._board._BLACK:
            pieceScore += (self._board._nbWHITE - self._board._nbBLACK) * 3 # score for white
        else:
            pieceScore += (self._board._nbBLACK - self._board._nbWHITE) * 3 # score for black

        liberties = 0
        score = 0
        for i in range(len(self._board)):
            if self._board[i] == self._board._EMPTY:
                pass
            elif self._board[i] == self._board.next_player():
                # Liberties
                string = self._board._getStringOfStone(i)
                liberties -= self._board._stringLiberties[string]*1
                # Corner + position
                score -= self.scores[i]*10
            else:
                # Liberties
                string = self._board._getStringOfStone(i)
                liberties += self._board._stringLiberties[string]*1
                # Corner + position
                score += self.scores[i]*10

        if self._board.next_player() == self._mycolor:
            pieceScore *= -1
            liberties *= -1
            score *= -1

        
        return pieceScore * normal(1, 0.1) + score * normal(1, 0.1) + liberties * normal(1, 0.1)