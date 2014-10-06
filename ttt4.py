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
import graphics as gr

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

def draw_board (board):
    for i,p in enumerate(board):
        if p != '.':
            WINDOW[i].setText(p)

def draw_initial_board (board):
    span = range(4)
    WINDOW['canvas'] = gr.GraphWin('Game Board', 279, 330, autoflush=True)
    for i in span:
        for j in span:
            r = gr.Rectangle(gr.Point(70*i,70*j), gr.Point(70*(i+1),70*(j+1)))
            r.draw(WINDOW['canvas'])
            t = gr.Text(r.getCenter(), '')
            t.setSize(30)
            t.draw(WINDOW['canvas'])
            WINDOW[4*j+i] = t
    s = gr.Text(gr.Point(140, 305), '')
    s.draw(WINDOW['canvas'])
    WINDOW['status'] = s

def read_player_input (board, player):
    move = int(raw_input('Make your move, {} (0-15): '.format(player)))
    if board[move] != '.':
        print 'Invalid move'
        return read_player_input(board, player)
    tuple_mve = (move%4 + 1, move/4 + 1)
    return tuple_mve

def wait_player_input (board, player):
    WINDOW['status'].setText('Click to place your {}'.format(player))
    clk_pt = WINDOW['canvas'].getMouse()
    ptx = clk_pt.getX()
    pty = clk_pt.getY()
    dist = []
    for i in range(16):
        pt = WINDOW[i].getAnchor()
        d2 = (ptx - pt.getX())**2 + (pty - pt.getY())**2
        dist.append(d2)
    move = dist.index(min(dist))
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

def mirror_brd (brd, dirc):
    h_inds = [3, 2, 1, 0, 7, 6, 5, 4, 11, 10, 9, 8, 15, 14, 13, 12]
    v_inds = [12, 13, 14, 15, 8, 9, 10, 11, 4, 5, 6, 7, 0, 1, 2, 3]
    if dirc == 'h':
        return [brd[i] for i in h_inds]
    elif dirc == 'v':
        return [brd[i] for i in v_inds]
    return brd

def get_all_equiv (brd):
    equivs = []
    tmp_brd = brd[:]
    mir_dirs = ['v', 'h']
    mir_ind = 0
    for i in range(4):
        tmp_brd = rotate_brd(tmp_brd)
        equivs.append(tmp_brd)
        tmp_brd = mirror_brd(tmp_brd, mir_dirs[mir_ind])
        mir_ind = +(not mir_ind)
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
    try:
        WINDOW['status'].setText('Computer player {} is thinking'.format(player))
    except Exception, e:
        pass
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

    best = vals.index(fun(vals))
    return possibilities[best]

def other (player):
    if player == 'X':
        return 'O'
    return 'X'

def run (initial_brd_str,player,playX,playO): 
    try:
        board = create_board(initial_brd_str)

        draw_initial_board(board)

        while not done(board):
            if player == 'X':
                move = playX(board,player)
            elif player == 'O':
                move = playO(board,player)
            else:
                fail('Unrecognized player '+player)
            board = make_move(board,move,player)
            draw_board(board)
            player = other(player)

        winner = has_win(board)
        if winner:
            print winner,'wins!'
            WINDOW['status'].setText('{} wins! Press any key to quit.'.format(winner))
            WINDOW['canvas'].getKey()
        else:
            print 'Draw'
            WINDOW['status'].setText('Draw. Press any key to quit.')
            WINDOW['canvas'].getKey()

    except Exception,e:
        print e
    print len(CACHE)
    print '{} cached and {} calculated'.format(STATS['cached'], STATS['calced'])
        
def main ():
    run('.' * 16, 'X', read_player_input, computer_move)

CACHE = {
    'X...............': 0,
    '.X..............': 0,
    '.....X..........': 0,
    'O...............': 0,
    '.O..............': 0,
    '.....O..........': 0
}

STATS = {
    'cached': 0,
    'calced': 0
}

PLAYER_MAP = {
#if you want to play through cmd, change to read_player_input
    'human': wait_player_input,
    'computer': computer_move
}

WINDOW = {}

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
