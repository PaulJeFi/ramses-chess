import chess
from evaluation import mateValue, evaluate

mvv_lva = [
        0,      0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,

        0,    105, 205, 305, 405, 505, 605,  105, 205, 305, 405, 505, 605,
        0,    104, 204, 304, 404, 504, 604,  104, 204, 304, 404, 504, 604,
        0,    103, 203, 303, 403, 503, 603,  103, 203, 303, 403, 503, 603,
        0,    102, 202, 302, 402, 502, 602,  102, 202, 302, 402, 502, 602,
        0,    101, 201, 301, 401, 501, 601,  101, 201, 301, 401, 501, 601,
        0,    100, 200, 300, 400, 500, 600,  100, 200, 300, 400, 500, 600,

        0,    105, 205, 305, 405, 505, 605,  105, 205, 305, 405, 505, 605,
        0,    104, 204, 304, 404, 504, 604,  104, 204, 304, 404, 504, 604,
        0,    103, 203, 303, 403, 503, 603,  103, 203, 303, 403, 503, 603,
        0,    102, 202, 302, 402, 502, 602,  102, 202, 302, 402, 502, 602,
        0,    101, 201, 301, 401, 501, 601,  101, 201, 301, 401, 501, 601,
        0,    100, 200, 300, 400, 500, 600,  100, 200, 300, 400, 500, 600
    ]

def get_ordered_moves(board: chess.Board, captures_only: bool=False) -> list :
    '''Move orderings'''
    
    # Étape 1 : trier les captures selon MVV LVA
    capture_moves = board.generate_legal_captures()

    move_list = []
    for move in capture_moves :
        try :
            move_list.append({
                    'move': move,
                    'cp': mvv_lva[
                                board.piece_at(move.from_square).piece_type * 13 +
                                board.piece_at(move.to_square).piece_type
                            ]
                })
        except AttributeError : # cas d'une prise en passant, la pièce capturée
             move_list.append({ # n'est pas sur la case d'arrivée
                    'move': move,
                    'cp': mvv_lva[
                                board.piece_at(move.from_square).piece_type * 13 +
                                chess.PAWN
                            ]
                })
        
    move_list = sorted(move_list, key=lambda k: k['cp'], reverse=True)

    # Étape 2 : ne retourner que les captures si quiecsence :
    if captures_only :
        return [move['move'] for move in move_list]

    # Étape 3 : savoir à partir d'où les captures ne sont pas bonnes (<= 150 cp)
    # pour insérer avant les autres coups :
    good_index = 0
    if len(move_list) != 0 :
        if not (True in move_list) :
            good_index = len(move_list) - 1
        else :
            good_index = len(move_list) - 1
            #good_index = [(move['cp'] <= 150) for move in move_list].index(True)

    # Étape 4 : insertion des autres coups
    castle = board.generate_castling_moves()
    move_list = [move['move'] for move in move_list]
    for move in board.legal_moves :
        if not (move in capture_moves) :
            # Si le coup est une promotion, il est probablement bon
            if move.promotion != None :
                move_list.insert(0, move)
            # Si le cou met en échec, il est aussi sans doute bon.
            elif board.gives_check(move) :
                move_list.insert(0, move)
            # Si le coup est un roque, il ne doit pas être mauvais
            elif move in castle :
                move_list.insert(0, move)
            else :
                move_list.insert(good_index, move)
            good_index += 1 # Update du good index (puisqu'on ajoute avant) 
    
    return move_list


class Search :

    def __init__(self, board=chess.Board, depth=3) -> None :
        self.board = board
        self.depth = depth
        self.nodes = 0
        self.pv = list(range(int((self.depth*self.depth + self.depth)/2)+1))
        self.base_number_of_moves = len(self.board.move_stack) # pour distance to mate dans quiesce
    
    def quiesce(self, alpha: float=-mateValue, beta: float=mateValue) -> float :
        '''Effectue une recherche de quiescence'''

        self.nodes += 1

        stand_pat = evaluate(self.board)
        moves = get_ordered_moves(self.board, True)

        # Fin de ligne
        if len(moves) == 0 :
            if not bool(self.board.legal_moves) :
                if self.board.is_checkmate() :
                    return -mateValue + (self.base_number_of_moves - len(self.board.move_stack))
                return 0

        # Mate distance pruning
        # Upper bound
        mating_value = mateValue - (self.base_number_of_moves - len(self.board.move_stack))
        if mating_value <= beta :
            beta = mating_value
            if alpha >= mating_value :
                return mating_value
        # Lower bound
        mating_value = mating_value = -mateValue + (self.base_number_of_moves - len(self.board.move_stack))
        if mating_value >= alpha :
            alpha = mating_value
            if beta <= mating_value : 
                return mating_value

        if  stand_pat >= beta :
            return beta
        if alpha < stand_pat :
            alpha = stand_pat

        for move in moves :
            self.board.push(move)
            score = -self.quiesce(-beta, -alpha)
            self.board.pop()

            if score >= beta :
                return beta
            if score > alpha :
                alpha = score

        return alpha

    def zwSearch(self, beta: float, depth: int) -> float :
        '''fail-hard zero window search, returns either beta-1 or beta'''

        self.nodes += 1

        alpha = beta - 1
        # this is either a cut- or all-node

        # Mate distance pruning
        # Upper bound
        mating_value = mateValue - (self.depth - depth)
        if mating_value <= beta :
            beta = mating_value
            if alpha >= mating_value :
                return mating_value
        # Lower bound
        mating_value = mating_value = -mateValue + (self.depth - depth)
        if mating_value >= alpha :
            alpha = mating_value
            if beta <= mating_value : 
                return mating_value

        moves = get_ordered_moves(self.board)

        # Fin de ligne
        if not bool(moves) :
            if self.board.is_checkmate() :
                return mating_value # pour distance to mate
            return 0

        if depth == 0 :
            return self.quiesce(beta-1, beta)

        for move in moves :
            self.board.push(move)
            score = -self.zwSearch(1-beta, depth - 1)
            self.board.pop()
            if score >= beta :
                return beta # fail-hard beta-cutoff

        return beta-1 # fail-hard, return alpha


    def pvSearch(self, alpha: float=-mateValue, beta: float=mateValue, depth=3, pvIndex: int=0) -> float :

        self.nodes += 1

        moves = get_ordered_moves(self.board)

        # Mate distance pruning
        # Upper bound
        mating_value = mateValue - (self.depth - depth)
        if mating_value <= beta :
            beta = mating_value
            if alpha >= mating_value :
                return mating_value
        # Lower bound
        mating_value = mating_value = -mateValue + (self.depth - depth)
        if mating_value >= alpha :
            alpha = mating_value
            if beta <= mating_value : 
                return mating_value

        # Fin de ligne
        if not bool(moves) :
            if self.board.is_checkmate() :
                return mating_value # pour distance to mate
            return 0

        if depth == 0 :
            return self.quiesce(alpha, beta)

        # PV store initialisation :
        self.pv[pvIndex] = 0 # no pv yet
        pvNextIndex = pvIndex + depth

        bSearchPv = True
        for move in moves :
            self.board.push(move)
            if bSearchPv :
                score = -self.pvSearch(-beta, -alpha, depth - 1, pvNextIndex)
            else :
                score = -self.zwSearch(-alpha, depth - 1)
                if ( score > alpha ) : # in fail-soft ... && score < beta ) is common
                    score = -self.pvSearch(-beta, -alpha, depth - 1, pvNextIndex) # re-search
            self.board.pop()

            if  score >= beta :
                return beta # fail-hard beta-cutoff
            if score > alpha :
                alpha = score # alpha acts like max in MiniMax
                bSearchPv = False   # *1)

                # PV store :
                self.pv[pvIndex] = move

        return alpha