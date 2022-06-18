import chess

pawnValue = 100
knightValue = 300
bishopValue = 320
rookValue = 500
queenValue = 900
kingValue = 20_000

mateValue = 100_000_000_000-1

BISHOP_PAIR_BONNUS = 0.5

CASTLE_BONNUS = 100
GOOD_CASTLE_BONNUS = 300
OPEN_FILE_CASTLE_MALUS = 250
KING_ON_OPEN_FILE_MALUS = 100
FIANCHETTO_BONNUS = 50

SHORT_CASTLE = (chess.G1, chess.G2, chess.H1, chess.H2, chess.G8, chess.G7, chess.H8, chess.H7)
LONG_CASTLE = (chess.A1, chess.B1, chess.C1, chess.A2, chess.B2, chess.C2,
               chess.A8, chess.B8, chess.C8, chess.A7, chess.B7, chess.C7)
SHORT_PAWN_PROTECTION_W = (chess.F2, chess.G2, chess.H2,
                           chess.F3, chess.G3, chess.H3)
SHORT_PAWN_PROTECTION_B = (chess.F8, chess.G8, chess.H8,
                           chess.F7, chess.G7, chess.H7)
LONG_PAWN_PROTECTION_W = (chess.A2, chess.B2, chess.C2,
                          chess.A3, chess.B3, chess.C3)
LONG_PAWN_PROTECTION_B = (chess.A7, chess.B7, chess.C7,
                          chess.A8, chess.B8, chess.C8)


K = [-30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
     20, 20,  0,  0,  0,  0, 20, 20,
     20, 30, 10,  0,  0, 10, 30, 20]

K_end = [-50,-40,-30,-20,-20,-30,-40,-50,
        -30,-20,-10,  0,  0,-10,-20,-30,
        -30,-10, 20, 30, 30, 20,-10,-30,
        -30,-10, 30, 40, 40, 30,-10,-30,
        -30,-10, 30, 40, 40, 30,-10,-30,
        -30,-10, 20, 30, 30, 20,-10,-30,
        -30,-30,  0,  0,  0,  0,-30,-30,
        -50,-30,-30,-30,-30,-30,-30,-50]

Q = [-20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
     -5,  0,  5,  5,  5,  5,  0, -5,
      0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20]

R = [ 0,  0,  0,  0,  0,  0,  0,  0,
      5, 10, 10, 10, 10, 10, 10,  5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
      0,  0,  0,  5,  5,  0,  0,  0]

N = [-50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50]

B = [20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20]

P = [ 0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5, -5,-10,  0,  0,-10, -5,  5,
    5, 10, 10,-20,-20, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0]

pqst_table = {chess.KING: [K, K_end],
            chess.QUEEN: Q,
            chess.ROOK: R,
            chess.KNIGHT: N,
            chess.BISHOP: B,
            chess.PAWN: P}


def popcount(a: int) -> int :
    return bin(a).count("1")

def scale_to_white_view(board: chess.Board, eval: float) -> float :
    perspective = 1 if board.turn == chess.WHITE else -1
    return eval * perspective

def evaluate(board: chess.Board=chess.Board()) -> float :

    '''
    if len(list(board.legal_moves)) == 0 :
        if board.is_check() :
            return -mateValue + 1 # +1 pour la recherche de mats courts
        return 0
    '''

    whiteEval = 0
    blackEval = 0

    endgameWeight = game_phase(board)
    pqst_evalu = pqst_eval(board, endgameWeight)

    whiteEval += countMaterial(board, chess.WHITE)
    blackEval += countMaterial(board, chess.BLACK)

    whiteEval += pqst_evalu[0]
    blackEval += pqst_evalu[1]

    mob = mobility(board)
    whiteEval += mob[0]
    blackEval += mob[1]

    whiteEval += bishop_pair(board, chess.WHITE)
    blackEval += bishop_pair(board, chess.BLACK)

    # whiteEval += king_safety(board, chess.WHITE, endgameWeight) * 0.3
    # blackEval += king_safety(board, chess.BLACK, endgameWeight) * 0.3

    evaluation = whiteEval-blackEval

    perspective = 1 if board.turn == chess.WHITE else -1

    return evaluation * perspective

def countMaterial(board: chess.Board=chess.Board(), color: chess.Color=chess.WHITE) -> float :
    material = 0
    material += len(board.pieces(chess.PAWN, color)) * pawnValue
    material += len(board.pieces(chess.KNIGHT, color)) * knightValue
    material += len(board.pieces(chess.BISHOP, color)) * bishopValue
    material += len(board.pieces(chess.ROOK, color)) * rookValue
    material += len(board.pieces(chess.QUEEN, color)) * queenValue
    return material

def pqst_eval(board: chess.Board, endgame_value: int) -> tuple :
    white_eval = 0
    black_eval = 0
    for square in chess.SQUARES :
        piece = board.piece_at(square)
        if piece != None :
            if piece.color :
                if piece.piece_type == chess.KING :
                    white_eval += ((pqst_table[piece.piece_type][0][63 - square] * (256 - endgame_value)) + (pqst_table[piece.piece_type][1][63 - square] * endgame_value)) / 256
                else :
                    white_eval += pqst_table[piece.piece_type][63 - square]
            else :
                if piece.piece_type == chess.KING :
                    black_eval += ((pqst_table[piece.piece_type][0][square] * (256 - endgame_value)) + (pqst_table[piece.piece_type][1][square] * endgame_value)) / 256
                else :
                    black_eval += pqst_table[piece.piece_type][square]
    return white_eval, black_eval

def game_phase(board: chess.Board) -> int :
    '''De 0.5 (ouv) à 256.5 (endg)'''
    PawnPhase = 0
    KnightPhase = 1
    BishopPhase = 1
    RookPhase = 2
    QueenPhase = 4
    TotalPhase = PawnPhase*16 + KnightPhase*4 + BishopPhase*4 + RookPhase*4 + QueenPhase*2

    phase = TotalPhase

    phase -= popcount(board.pawns) * PawnPhase
    phase -= popcount(board.knights) * KnightPhase
    phase -= popcount(board.bishops) * KnightPhase
    phase -= popcount(board.rooks) * RookPhase
    phase -= popcount(board.queens) * QueenPhase

    phase = (phase * 256 + (TotalPhase / 2)) / TotalPhase
    return phase

def mobility(board: chess.Board) -> int :

    w_mob = 0
    b_mob = 0
    occupied = board.occupied

    for square in chess.SQUARES :

        piece = board.piece_at(square)
        if piece == None :
            continue

        if piece.color :
            w_mob += mobility_square(square, piece.piece_type, occupied)
        else :
            b_mob += mobility_square(square, piece.piece_type, occupied)

    return w_mob, b_mob


def mobility_square(square: chess.Square, piece: chess.Piece, occupied: int) -> int: 

    if piece == None : return 0

    if piece == chess.ROOK :
        return popcount((chess.BB_RANK_ATTACKS[square][chess.BB_RANK_MASKS[square] & occupied] | chess.BB_FILE_ATTACKS[square][chess.BB_FILE_MASKS[square] & occupied]) & ~occupied)

    if piece == chess.KNIGHT :
        return popcount(chess.BB_KNIGHT_ATTACKS[square]  & ~occupied )

    if piece == chess.BISHOP :
        return popcount(chess.BB_DIAG_ATTACKS[square][chess.BB_DIAG_MASKS[square] & occupied] & ~occupied)

    if piece == chess.QUEEN :
        return popcount((chess.BB_RANK_ATTACKS[square][chess.BB_RANK_MASKS[square] & occupied] |
          chess.BB_FILE_ATTACKS[square][chess.BB_FILE_MASKS[square] & occupied] |
          chess.BB_DIAG_ATTACKS[square][chess.BB_DIAG_MASKS[square] & occupied]) & ~occupied)

    return 0


def bishop_pair(board: chess.Board, color: chess.Color) :
    if len(board.pieces(chess.BISHOP, color)) == 2 :
        return BISHOP_PAIR_BONNUS
    return 0


def king_safety(board: chess.Board, color: chess.Color, endgame_weight) :

    # TODO : pawn storm
    
    score = 0
    king = board.king(color)
    eg_factor = (256.5- endgame_weight)/256.5

    if color : # Si Blancs
        # Test petit roque
        if king in SHORT_CASTLE :
            score += CASTLE_BONNUS

            if bool(board.pawns & 0x700) & bool(board.pawns & 0x10600) & bool(board.pawns & 0x20500) : # Si tous les pions protègent le roque
                score += GOOD_CASTLE_BONNUS

            else :
                # max pour éviter que tous les pions se mettent devant le roi
                score -= OPEN_FILE_CASTLE_MALUS * (max((1-popcount(board.pawns & 0x40400)) + (1-popcount(board.pawns & 0x20200)) + (1-popcount(board.pawns & 0x10100)), 0))
   
            if (board.bishops & 0x200) : # Fianchetto
                    score += FIANCHETTO_BONNUS

        # Test grand roque
        elif king in LONG_CASTLE :
            score += CASTLE_BONNUS

            if bool(board.pawns & 0xe000) & bool(board.pawns & 0x40a000) & bool(board.pawns & 0x806000) : # Si tous les pions protègent le roque
                score += GOOD_CASTLE_BONNUS
            else :
                # max pour éviter que tous les pions se mettent devant le roi
                score -= OPEN_FILE_CASTLE_MALUS * (max((1-popcount(board.pawns & 0x808000)) + (1-popcount(board.pawns & 0x404000)) + (1-popcount(board.pawns & 0x202000)), 0))

            if (board.bishops & 0x4000) : # Fianchetto
                    score += FIANCHETTO_BONNUS

        # Roi non-roqué ou déroqué
        else :
            file = chess.square_file(king)
            my_pawn_type = chess.Piece(chess.PAWN, color)
            for square in chess.SQUARES :
                if chess.square_file(square) == file :
                    piece = board.piece_at(square)
                    if piece == my_pawn_type :
                        score += KING_ON_OPEN_FILE_MALUS * eg_factor
                        break
            score -= KING_ON_OPEN_FILE_MALUS * eg_factor

    elif not color : # Si Noirs
        # Test petit roque
        if king in SHORT_CASTLE :
            score += CASTLE_BONNUS

            if bool(board.pawns & 0x7000000000000) & bool(board.pawns & 0x5020000000000) & bool(board.pawns & 0x6010000000000) : # Si tous les pions protègent le roque
                score += GOOD_CASTLE_BONNUS
            else :
                # max pour éviter que tous les pions se mettent devant le roi
                score -= OPEN_FILE_CASTLE_MALUS * (max((1-popcount(board.pawns & 0x4040000000000)) + (1-popcount(board.pawns & 0x2020000000000)) + (1-popcount(board.pawns & 0x1010000000000)), 0))

            if (board.bishops & 0x2000000000000) : # Fianchetto
                        score += FIANCHETTO_BONNUS

        # Test grand roque
        elif king in LONG_CASTLE :
            score += CASTLE_BONNUS

            if bool(board.pawns & 0xe0000000000000) & bool(board.pawns & 0x60800000000000) & bool(board.pawns & 0xa0400000000000) : # Si tous les pions protègent le roque
                score += GOOD_CASTLE_BONNUS
            else :
                # max pour éviter que tous les pions se mettent devant le roi
                score -= OPEN_FILE_CASTLE_MALUS * (max((1-popcount(board.pawns & 0x80800000000000)) + (1-popcount(board.pawns & 0x40400000000000)) + (1-popcount(board.pawns & 0x20200000000000)), 0))

            if (board.bishops & 0x40000000000000) : # Fianchetto
                    score += FIANCHETTO_BONNUS

        # Roi non-roqué ou déroqué
        else :
            file = chess.square_file(king)
            my_pawn_type = chess.Piece(chess.PAWN, color)
            for square in chess.SQUARES :
                if chess.square_file(square) == file :
                    piece = board.piece_at(square)
                    if piece == my_pawn_type :
                        score += KING_ON_OPEN_FILE_MALUS * eg_factor
                        break
            score -= KING_ON_OPEN_FILE_MALUS * eg_factor

    
    return score


if __name__ == '__main__' :
    import random
    def random_board(max_depth=200):
        board = chess.Board()
        depth = random.randrange(0, max_depth)
        for _ in range(depth):
            all_moves = list(board.legal_moves)
            random_move = random.choice(all_moves)
            board.push(random_move)
            if board.is_game_over():
                break
        return board

    #board = random_board()
    board = chess.Board('r1bk1b1r/ppp2ppp/2n2n2/1B2p3/4P3/5N2/PPP2PPP/RNB1K2R w KQ - 2 7')
    print(f'\nfen {board.fen()}\n\nLichess link : https://lichess.org/analysis/standard/{board.fen().replace(" ", "_")}\nstatic eval (cp) : {int(scale_to_white_view(board, evaluate(board)))}\n')
