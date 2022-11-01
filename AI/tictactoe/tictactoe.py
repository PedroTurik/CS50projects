"""
Tic Tac Toe Player
"""

import math
from socket import TIPC_SUBSCR_TIMEOUT
from xml.dom.minidom import Element
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    x_count = o_count = 0
    for row in board:
        for element in row:
            if element == X: x_count += 1
            if element == O: o_count += 1
    if x_count == o_count:
        return X
    else:
        return O

def actions(board):
    possible_actions = set()
    for i, row in enumerate(board):
        for j, element in enumerate(row):
            if element == EMPTY:
                possible_actions.add((i,j))
    return possible_actions



def result(board, action):
    new_board = deepcopy(board)
    r, c = action
    if new_board[r][c] != EMPTY:
        raise Exception("Impossible move")
    new_board[r][c] = player(new_board)
    return new_board

def winner(board):
    for key in [X, O]:
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] == key:
                return key
            if board[0][i] == board[1][i] == board[2][i] == key:
                return key
        for j in [0,2]:
            if board[0][j] == board[1][1] == board[2][2-j] == key:
                return key
    return None



def terminal(board):
    if winner(board): 
        return True
    for row in board:
        for element in row:
            if element == EMPTY: return False
    return True





def utility(board):
    win = winner(board)
    if win:
        return 1 if win == X else -1
    else:
        return 0

def minimax(board):
    if terminal(board): 
        return None
    max_or_min = max if player(board) == X else min
    possible_actions = actions(board)
    
    def playing(board, act):
        new_board =  result(board, act)
        mm = max if player(new_board) == X else min
        if terminal(new_board):
            return utility(new_board)
        new_acts = actions(new_board)
        return mm([playing(new_board, x) for x in new_acts])

    return max_or_min(possible_actions, key=lambda x: playing(board, x))
        
