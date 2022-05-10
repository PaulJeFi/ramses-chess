import chess

pawnValue = 100
knightValue = 320 # 300
bishopValue = 330 # 300
rookValue = 500
queenValue = 900
kingValue = 20_000

mateValue = 100_000_000_000-1

def popcount(a: int) -> int :
    return bin(a).count("1")

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

def scale_to_white_view(board: chess.Board, eval: float) -> float :
    perspective = 1 if board.turn == chess.WHITE else -1
    return eval * perspective

def evaluate(board: chess.Board=chess.Board()) -> float :

    if len(list(board.legal_moves)) == 0 :
        if board.is_check() :
            return -mateValue + 1 # +1 pour la recherche de mats courts
        return 0

    endgameWeight = game_phase(board)
    pqst_evalu = pqst_eval(board, endgameWeight)

    whiteEval = 0
    blackEval = 0

    whiteEval += countMaterial(board, chess.WHITE)
    blackEval += countMaterial(board, chess.BLACK)

    whiteEval += pqst_evalu[0]
    blackEval += pqst_evalu[1]

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

def game_phase(board: chess.Board) -> int :
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