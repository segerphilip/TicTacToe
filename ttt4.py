#!/usr/bin/env python
# 

#
# Game Programming, Level 2 Project
#
# TIC-TAC-TOE 4
#
# A simple strategy game, an extension of the standard 3x3 tic-tac-toe
#
# Devs: Jacob Kingery
#       Philip Seger

import sys


def fail (msg):
    raise StandardError(msg)


def create_board (s):
    board = list(s)
    return board

def has_mark (board,x,y):
    index = (x-1) + 4*(y-1)
    if board[index] == '.':
        return False
    return board[index]

def has_win (board):
    win_sequences = [
                    [0,1,2,3],
                    [4,5,6,7],
                    [8,9,10,11],
                    [12,13,14,15],
                    [0,4,8,12],
                    [1,5,9,13],
                    [2,6,10,14],
                    [3,7,11,15],
                    [0,5,10,15],
                    [3,6,9,12]
                    ]

    mark_value = {'O':1, '.':0, 'X':10}
    for positions in win_sequences:
        s = sum(mark_value[board[pos]] for pos in positions)
        if s == 4:
            return 'O'
        if s == 40:
            return 'X'
    return False

def done (board):
    return (has_win(board) or '.' not in board)

def print_board (board):
    for i in range(4):
        print '',board[i*4],'|',board[i*4+1],'|',board[i*4+2],'|',board[i*4+3]
        print '-'*15*(i!=3)

def read_player_input (board, player):
    move = int(raw_input('Make your move, {} (0-15): '.format(player)))
    if board[move] != '.':
        print 'Invalid move'
        return read_player_input(board, player)
    tuple_mve = (move % 4 + 1, move / 4 + 1)
    return tuple_mve

def make_move (board,move,player):
    x,y = move
    copy_brd = board[:]
    index = (x-1) + 4*(y-1)
    copy_brd[index] = player
    return copy_brd

def computer_move (board,player):
    # FIX ME
    #
    # Select a move for the computer, when playing as 'player' (either 
    #   'X' or 'O')
    # Return the selected move (a tuple (x,y) with each position between 
    #   1 and 4)
    return None


def other (player):
    if player == 'X':
        return 'O'
    return 'X'


def run (str,player,playX,playO): 

    board = create_board(str)

    print_board(board)

    while not done(board):
        if player == 'X':
            move = playX(board,player)
        elif player == 'O':
            move = playO(board,player)
        else:
            fail('Unrecognized player '+player)
        board = make_move(board,move,player)
        print_board(board)
        player = other(player)

    winner = has_win(board)
    if winner:
        print winner,'wins!'
    else:
        print 'Draw'
        
def main ():
    run('.' * 16, 'X', read_player_input, computer_move)


PLAYER_MAP = {
    'human': read_player_input,
    'computer': computer_move
}

if __name__ == '__main__':

    try:
        str = sys.argv[1] if len(sys.argv)>1 else '.' * 16
        if len(str) != 16:
            print 'Your board is the wrong length'
            exit(1)
        player = sys.argv[2] if len(sys.argv)>3 else 'X'
        playX = PLAYER_MAP[sys.argv[3]] if len(sys.argv)>3 else read_player_input
        playO = PLAYER_MAP[sys.argv[4]] if len(sys.argv)>4 else computer_move
    except:
        print 'Usage: %s [starting board] [X|O] [human|computer] [human|computer]' % (sys.argv[0])
        exit(1)
    run(str,player,playX,playO)


