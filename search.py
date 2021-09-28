import chess
import eval
from move_generation import get_ordered_moves, move_value
import transposition
import time


def quiesce(pos, alpha, beta, depth=4) :
    '''Effecture une recherche de quiescence.'''
    stand_pat = eval.evaluation_turn(pos)
    #return stand_pat # Uncommenter cette ligne pour un moteur moins performant mais plus rapide.
    if stand_pat >= beta :
        return beta
    if alpha < stand_pat:
        alpha = stand_pat
    if depth >= 0 :
        for move in get_ordered_moves(pos) :
            if pos.is_capture(move) :
                pos.push(move)        
                score = -quiesce(pos, -beta, -alpha, depth-1)
                pos.pop()
                if score >= beta :
                    return beta
                if score > alpha :
                    alpha = score  
    return alpha

# https://www.chessprogramming.org/Principal_Variation_Search
def pvSearch(board, alpha, beta, depth) :
    '''PrincipaL Variation Search'''
    if (depth == 0) :
        return quiesce(board, alpha, beta)
    bSearchPv = True
    for move in get_ordered_moves(board) :
        board.push(move)
        if bSearchPv :
            score = -pvSearch(board, -beta, -alpha, depth-1)
        else :
            score = -zwSearch(board, -alpha, depth - 1)
            if (score > alpha) : # in fail-soft ... && score < beta ) is common
                score = -pvSearch(board, -beta, -alpha, depth-1) # re-search
        board.pop()
        if (score >= beta) :
            return beta   # fail-hard beta-cutoff
        if (score > alpha) :
            alpha = score # alpha acts like max in MiniMax
            bSearchPv = False   # *1)
    return alpha

# fail-hard zero window search, returns either beta-1 or beta
def zwSearch(board, beta, depth) :
    '''Zero Window Search'''
    # alpha == beta - 1
    # this is either a cut- or all-node
    if (depth == 0) :
        return quiesce(board, beta-1, beta)
    for move in get_ordered_moves(board)  :
        board.push(move)
        score = -zwSearch(board, 1-beta, depth-1)
        board.pop()
        if (score >= beta) :
            return beta   # fail-hard beta-cutoff
    return beta-1 # fail-hard, return alpha


def PVS_root(depth: int, board: chess.Board, moves=None, t0=0) -> chess.Move:
    '''Retourne le meilleur coup accompagné de son évaluation.'''
    maximize = board.turn == chess.WHITE
    best_move = -float("inf")
    if not maximize:
        best_move = float("inf")

    if moves == None :
        moves = get_ordered_moves(board)
    best_move_found = moves[0]
    nodes = 0
    if t0 == 0 :
        t0 = time.time()

    for move in moves :
        board.push(move)
        if board.can_claim_draw():
            value = 0.0
        else :
            value = transposition.find_eval(board, depth)
            if value == None :
                value = pvSearch(board, -float("inf"), float("inf"), depth-1)
                if board.turn == chess.WHITE :
                    pass
                else :
                    value = -value
                if not maximize :
                    evalu = -value
                else :
                    evalu = value
                transposition.add_eval(board, depth, evalu)
            elif not maximize :
                value = -value
        board.pop()
        if maximize and value >= best_move :
            best_move = value
            best_move_found = move
        elif not maximize and value <= best_move :
            best_move = value
            best_move_found = move
        nodes += 1
        print(f'info depth {depth} score cp {round(arround(best_move)*100)} nodes {nodes} time {round(1000 * (time.time() - t0))} pv {str(best_move_found)}')
        # Pour l'instant, les nodes ne sont pas des vrais nodes.

    return best_move_found, best_move

def iterative_deepening(board, Depth) :
    depth = 1
    t0 = time.time()
    moves = get_ordered_moves(board)
    while depth != Depth :
        moves = move_ordering(board, depth, t0, moves)
        moves = moves[0:3]
        depth += 1
    return PVS_root(Depth, board, moves, t0)

def move_ordering(board, depth, t0=0, moves=None) :
    '''Pour les tests. Retourne les mouvements dans l'ordre par rapport à une depth données.'''
    if t0 == 0 :
        t0 = time.time()
    if moves == None :
        moves = get_ordered_moves(board)
    if board.turn == chess.WHITE :
        best_value = -float('inf')
    else :
        best_value = float('inf')
    best_move = moves[0]
    best_moves_values = []
    best_moves = []
    nodes = 0
    for move in moves :
        board.push(move)

        if board.can_claim_draw():
            value = 0.0
        
        else :
            value = transposition.find_eval(board, depth)
            if value == None :
                value = pvSearch(board, -float("inf"), float("inf"), depth-1)
                if board.turn == chess.WHITE :
                    pass
                else :
                    value = -value
                transposition.add_eval(board, depth, value)
            else :
                pass
            best_moves.append(move)
            best_moves_values.append(value)
        nodes += 1
        print(f'info depth {depth} score cp {round(arround(best_value)*100)} nodes {nodes} time {round(1000 * (time.time() - t0))} pv {str(best_move)}')
        board.pop()
        if board.turn == chess.WHITE :
            if value > best_value :
                    best_value = value
                    best_move = move
        else :
            if value < best_value :
                    best_value = value
                    best_move = move

    #print(f'\n{[round(value) for value in best_moves_values]}\n{[str(move) for move in best_moves]}\n')
    return sorted(best_moves, key=lambda m: best_moves_values[best_moves.index(m)], reverse=board.turn)
    

def arround(value) :
    '''Permet de retourner la valeur de mat numériquement.'''
    if value == float('inf') :
        return 10000000000
    elif value == -float('inf') :
        return -10000000000
    else :
        return value

def search(board, depth) :
    '''On part de l'hypothèse que le meilleur coup en profondeur n se retrouve
    dans les trois meilleurs coups en profondeur n. Cette hypothèse est vraie
    63 % du temps (sans quiescence) et divise le temps de recherche par 11
    si on ne prend que les trois meilleurs coups.'''
    t0 = time.time()
    conj = move_ordering(board, depth-1, t0)
    if len(conj) >= 3 :
        conj = conj[0:3]
    move, value = PVS_root(depth, board, conj, t0)
    return move, value