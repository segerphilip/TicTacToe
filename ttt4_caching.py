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
import shelve

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
    tuple_mve = (move%4 + 1, move/4 + 1)
    return tuple_mve

def make_move (board, move, player):
    x,y = move
    copy_brd = board[:]
    index = (x-1) + 4*(y-1)
    copy_brd[index] = player
    return copy_brd

def possible_moves (board):
    return [(i%4 + 1, i/4 + 1) for i, e in enumerate(board) if e == '.']

def utility (board):
    p = has_win(board)
    return 0 + (p=='X') - (p=='O')

def rotate_brd (brd):
    rot_inds = [12, 8, 4, 0, 13, 9, 5, 1, 14, 10, 6, 2, 15, 11, 7, 3]
    return [brd[i] for i in rot_inds]

def mirror_brd (brd):
    mir_inds = [3, 2, 1, 0, 7, 6, 5, 4, 11, 10, 9, 8, 15, 14, 13, 12]
    return [brd[i] for i in mir_inds]

def get_all_equiv (brd):
    equivs = []
    tmp_brd = brd[:]
    for i in range(4):
        tmp_brd = rotate_brd(tmp_brd)
        equivs.append(tmp_brd)
        tmp_brd = mirror_brd(tmp_brd)
        equivs.append(tmp_brd)
    return equivs

def cache_or_calc (brd, minimax):
    equiv_brds = get_all_equiv(brd)
    for eq_brd in equiv_brds:
        try:
            eq_str_brd = ''.join(eq_brd)
            v = CACHE[eq_str_brd]
            STATS['cached'] += 1
            return v
        except:
            pass
    str_brd = ''.join(brd)
    v = minimax(brd)
    CACHE[str_brd] = v
    STATS['calced'] += 1
    return v

def min_value (board):
    if done(board):
        return utility(board)

    v = 2
    for move in possible_moves(board):
        new_brd = make_move(board, move, 'O')
        v = min(v, cache_or_calc(new_brd, max_value))

    return v

def max_value (board):
    if done(board):
        return utility(board)

    v = -2
    for move in possible_moves(board):
        new_brd = make_move(board, move, 'X')
        v = max(v, cache_or_calc(new_brd, min_value))

    return v

def computer_move (board, player):
    vals = []
    minimax = max_value
    fun = min
    if player == 'X':
        minimax = min_value
        fun = max

    possibilities = possible_moves(board)
    for move in possibilities:
        new_brd = make_move(board, move, player)

        v = cache_or_calc(new_brd, minimax)

        vals.append(v)
        print 'Move {} for player {} has minimax value {}'.format(move, player, v)
        if fun(vals) == fun((-1, 1)):
            break

    # print possibilities
    # print vals

    best = vals.index(fun(vals))
    return possibilities[best]

def other (player):
    if player == 'X':
        return 'O'
    return 'X'

def run (initial_brd_str,player,playX,playO): 
    try:
        board = create_board(initial_brd_str)

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
    except Exception,e:
        print e
    print len(CACHE)
    CACHE.close()
    print '{} cached and {} calculated'.format(STATS['cached'], STATS['calced'])
        
def main ():
    run('.' * 16, 'X', read_player_input, computer_move)


CACHE = shelve.open('ttt_cache')
STATS = {
    'cached': 0,
    'calced': 0
}

PLAYER_MAP = {
    'human': read_player_input,
    'computer': computer_move
}

if __name__ == '__main__':
    try:
        initial_brd_str = sys.argv[1] if len(sys.argv)>1 else '.' * 16
        if len(initial_brd_str) != 16:
            print 'Your board is the wrong length'
            exit(1)
        player = sys.argv[2] if len(sys.argv)>3 else 'X'
        playX = PLAYER_MAP[sys.argv[3]] if len(sys.argv)>3 else read_player_input
        playO = PLAYER_MAP[sys.argv[4]] if len(sys.argv)>4 else computer_move
    except:
        print 'Usage: %s [starting board] [X|O] [human|computer] [human|computer]' % (sys.argv[0])
        exit(1)
    run(initial_brd_str,player,playX,playO)
