import chess
import stockfish_book
import search
from move_generation import get_ordered_moves
from tablebase_online import tablebase

import time
import evaluation

def iterative_deepening(board: chess.Board, depth: int) -> tuple :

    # Temps au debut
    start_time = time.time()
    curr_depth = 0
    nodes = 0

    # Move ordering avant la recherche
    tmp_moves = search.get_ordered_moves(board)

    # Premier meilleur coup (depth 0) :
    b_move = tmp_moves[0]
    board.push(b_move)
    b_score = evaluation.evaluate(board)
    scaled_score = evaluation.scale_to_white_view(board, b_score)
    board.pop()

    # uci report
    print(f'info depth {curr_depth} score cp {int(scaled_score)} nodes {0} nps 0 time {int((time.time()-start_time) * 1000)} pv {str(b_move)}')

    if depth < 1 :
        return b_move, scaled_score
    
    last_time = time.time()

    # Initialisation précise du move ordering : depth 1
    moves = []
    curr_depth += 1
    for move in tmp_moves :
        board.push(move)
        searcher = search.Search(board, curr_depth-1)
        tmp_value = searcher.pvSearch(depth=searcher.depth)
        board.pop()
        
        nodes += searcher.nodes
        moves.append((move, tmp_value))
    
    # Ordonner les coups :
    moves = sorted(moves, key=lambda x: x[1])

    # Retirer les doublons
    old_moves = moves
    moves = []
    tmp_moves = []
    for move, value in old_moves :
        if not (move in tmp_moves) :
            moves.append((move, value))
            tmp_moves.append(move)
    
    # Extraire le meilleur coup et son évaluation
    b_move = moves[0][0]
    board.push(b_move)
    scaled_score = evaluation.scale_to_white_view(board, moves[0][1])
    board.pop()

    # uci report
    for ind, (move, value) in enumerate(moves) :
        print(f'info depth {curr_depth} currmove {str(move)} currmovenumber {ind+1}') 
    print(f'info depth {curr_depth} score cp {int(scaled_score)} nodes {nodes} nps {int(nodes/(time.time()-last_time))} time {int((time.time()-last_time) * 1000)} pv {str(b_move)}')
    last_time = time.time()

    while curr_depth < depth :
        curr_depth += 1

        old_moves = moves
        moves = []
        new_nodes = 0
        for move, forget_this in old_moves :
            board.push(move)
            searcher = search.Search(board, curr_depth-1)
            tmp_value = searcher.pvSearch(depth=searcher.depth)
            board.pop()
            
            nodes += searcher.nodes
            new_nodes += searcher.nodes
            moves.append((move, tmp_value))
        
        # Ordonner les coups :
        moves = sorted(moves, key=lambda x: x[1])

        # Retirer les doublons
        old_moves = moves
        moves = []
        tmp_moves = []
        for move, value in old_moves :
            if not (move in tmp_moves) :
                moves.append((move, value))
                tmp_moves.append(move)
        
        # Extraire le meilleur coup et son évaluation
        b_move = moves[0][0]
        board.push(b_move)
        scaled_score = evaluation.scale_to_white_view(board, moves[0][1])
        board.pop()

        # uci report
        for ind, (move, value) in enumerate(moves) :
            print(f'info depth {curr_depth} currmove {str(move)} currmovenumber {ind+1}') 
        print(f'info depth {curr_depth} score cp {int(scaled_score)} nodes {nodes} nps {int(new_nodes/(time.time()-last_time))} time {int((time.time()-last_time)) * 1000} pv {str(b_move)}')
        last_time = time.time()

    return b_move, scaled_score

def best_move(board, timeleft=None, depth=2) :
    '''Détermine le meilleur coup.'''
    value = 0
    try :
        move = stockfish_book.move_from_book(board, stockfish_book.book)
        if move != None :
            return move, 0
    except Exception :
        pass
    move = tablebase(board)
    if move != None :
        return move, 0

    return iterative_deepening(board, 4)

def game_is_finished(pos) :
    '''Détermine si la partie est finie.'''
    if pos.is_checkmate() or pos.is_stalemate() or pos.is_insufficient_material() or pos.can_claim_threefold_repetition() :
        return True
    else :
        return False
