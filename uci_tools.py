import chess
from best_move import best_move as engine

def search(board, time=None, depth=2) :
    move, value = engine(board, depth=depth)
    if value != 'book' :
        print('info score cp', value*100)
    print('bestmove {move}'.format(move=move))
    return str(move)