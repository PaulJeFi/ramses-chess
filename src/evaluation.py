import chess
import random

SKILL = 20
GRAIN = 10

GRAIN = int(max(1, -GRAIN, GRAIN))

WPAWN   = chess.Piece(chess.PAWN,   chess.WHITE)
WKNIGHT = chess.Piece(chess.KNIGHT, chess.WHITE)
WBISHOP = chess.Piece(chess.BISHOP, chess.WHITE)
WROOK   = chess.Piece(chess.ROOK,   chess.WHITE)
WQUEEN  = chess.Piece(chess.QUEEN,  chess.WHITE)
WKING   = chess.Piece(chess.KING,   chess.WHITE)
BPAWN   = chess.Piece(chess.PAWN,   chess.BLACK)
BKNIGHT = chess.Piece(chess.KNIGHT, chess.BLACK)
BBISHOP = chess.Piece(chess.BISHOP, chess.BLACK)
BROOK   = chess.Piece(chess.ROOK,   chess.BLACK)
BQUEEN  = chess.Piece(chess.QUEEN,  chess.BLACK)
BKING   = chess.Piece(chess.KING,   chess.BLACK)


# VALUE[chess.PieceType] = (EG_PSQT, MG_PSQT, MG, EG, phase)
VALUES = {
    chess.PAWN: ([
    0,   0,   0,   0,   0,   0,  0,   0,
    98, 134,  61,  95,  68, 126, 34, -11,
    -6,   7,  26,  31,  65,  56, 25, -20,
    -14,  13,   6,  21,  23,  12, 17, -23,
    -27,  -2,  -5,  12,  17,   6, 10, -25,
    -26,  -4,  -4, -10,   3,   3, 33, -12,
    -35,  -1, -20, -23, -15,  24, 38, -22,
      0,   0,   0,   0,   0,   0,  0,   0],
    
    [
    0,   0,   0,   0,   0,   0,   0,   0,
    178, 173, 158, 134, 147, 132, 165, 187,
     94, 100,  85,  67,  56,  53,  82,  84,
     32,  24,  13,   5,  -2,   4,  17,  17,
     13,   9,  -3,  -7,  -7,  -8,   3,  -1,
      4,   7,  -6,   1,   0,  -5,  -1,  -8,
     13,   8,   8,  10,  13,   0,   2,  -7,
      0,   0,   0,   0,   0,   0,   0,   0], 92, 94, 0),

    chess.KNIGHT: ([
    -167, -89, -34, -49,  61, -97, -15, -107,
     -73, -41,  72,  36,  23,  62,   7,  -17,
     -47,  60,  37,  65,  84, 129,  73,   44,
      -9,  17,  19,  53,  37,  69,  18,   22,
     -13,   4,  16,  13,  28,  19,  21,   -8,
     -23,  -9,  12,  10,  19,  17,  25,  -16,
     -29, -53, -12,  -3,  -1,  18, -14,  -19,
    -105, -21, -58, -33, -17, -28, -19,  -23],
    
    [
    -58, -38, -13, -28, -31, -27, -63, -99,
    -25,  -8, -25,  -2,  -9, -25, -24, -52,
    -24, -20,  10,   9,  -1,  -9, -19, -41,
    -17,   3,  22,  22,  22,  11,   8, -18,
    -18,  -6,  16,  25,  16,  17,   4, -18,
    -23,  -3,  -1,  15,  10,  -3, -20, -22,
    -42, -20, -10,  -5,  -2, -20, -23, -44,
    -29, -51, -23, -15, -22, -18, -50, -64], 337, 281, 1),

    chess.BISHOP: ([
    -29,   4, -82, -37, -25, -42,   7,  -8,
    -26,  16, -18, -13,  30,  59,  18, -47,
    -16,  37,  43,  40,  35,  50,  37,  -2,
     -4,   5,  19,  50,  37,  37,   7,  -2,
     -6,  13,  13,  26,  34,  12,  10,   4,
      0,  15,  15,  15,  14,  27,  18,  10,
      4,  15,  16,   0,   7,  21,  33,   1,
    -33,  -3, -14, -21, -13, -12, -39, -21],
    
    [
    -14, -21, -11,  -8, -7,  -9, -17, -24,
     -8,  -4,   7, -12, -3, -13,  -4, -14,
      2,  -8,   0,  -1, -2,   6,   0,   4,
     -3,   9,  12,   9, 14,  10,   3,   2,
     -6,   3,  13,  19,  7,  10,  -3,  -9,
    -12,  -3,   8,  10, 13,   3,  -7, -15,
    -14, -18,  -7,  -1,  4,  -9, -15, -27,
    -23,  -9, -23,  -5, -9, -16,  -5, -17], 365, 297, 1),

    chess.ROOK: ([
     32,  42,  32,  51, 63,  9,  31,  43,
     27,  32,  58,  62, 80, 67,  26,  44,
     -5,  19,  26,  36, 17, 45,  61,  16,
    -24, -11,   7,  26, 24, 35,  -8, -20,
    -36, -26, -12,  -1,  9, -7,   6, -23,
    -45, -25, -16, -17,  3,  0,  -5, -33,
    -44, -16, -20,  -9, -1, 11,  -6, -71,
    -19, -13,   1,  17, 16,  7, -37, -26],
    
    [
    13, 10, 18, 15, 12,  12,   8,   5,
    11, 13, 13, 11, -3,   3,   8,   3,
     7,  7,  7,  5,  4,  -3,  -5,  -3,
     4,  3, 13,  1,  2,   1,  -1,   2,
     3,  5,  8,  4, -5,  -6,  -8, -11,
    -4,  0, -5, -1, -7, -12,  -8, -16,
    -6, -6,  0,  2, -9,  -9, -11,  -3,
    -9,  2,  3, -1, -5, -13,   4, -20], 477, 512, 2),

    chess.QUEEN: ([
    -28,   0,  29,  12,  59,  44,  43,  45,
    -24, -39,  -5,   1, -16,  57,  28,  54,
    -13, -17,   7,   8,  29,  56,  47,  57,
    -27, -27, -16, -16,  -1,  17,  -2,   1,
     -9, -26,  -9, -10,  -2,  -4,   3,  -3,
    -14,   2, -11,  -2,  -5,   2,  14,   5,
    -35,  -8,  11,   2,   8,  15,  -3,   1,
     -1, -18,  -9,  10, -15, -25, -31, -50],
     
     [
     -9,  22,  22,  27,  27,  19,  10,  20,
    -17,  20,  32,  41,  58,  25,  30,   0,
    -20,   6,   9,  49,  47,  35,  19,   9,
      3,  22,  24,  45,  57,  40,  57,  36,
    -18,  28,  19,  47,  31,  34,  39,  23,
    -16, -27,  15,   6,   9,  17,  10,   5,
    -22, -23, -30, -16, -16, -23, -36, -32,
    -33, -28, -22, -43,  -5, -32, -20, -41], 1025, 936, 4),

    chess.KING: ([
    -65,  23,  16, -15, -56, -34,   2,  13,
     29,  -1, -20,  -7,  -8,  -4, -38, -29,
     -9,  24,   2, -16, -20,   6,  22, -22,
    -17, -20, -12, -27, -30, -25, -14, -36,
    -49,  -1, -27, -39, -46, -44, -33, -51,
    -14, -14, -22, -46, -44, -30, -15, -27,
      1,   7,  -8, -64, -43, -16,   9,   8,
    -15,  36,  12, -54,   8, -28,  24,  14],
    
    [
    -74, -35, -18, -18, -11,  15,   4, -17,
    -12,  17,  14,  17,  17,  38,  23,  11,
     10,  17,  23,  15,  20,  45,  44,  13,
     -8,  22,  24,  27,  26,  33,  26,   3,
    -18,  -4,  21,  24,  27,  23,   9, -11,
    -19,  -3,  11,  21,  23,  16,   7,  -9,
    -27, -11,   4,  13,  14,   4,  -5, -17,
    -53, -34, -21, -11, -28, -14, -24, -43], 0, 0, 0)}

ISOLATED_MASK = [
    chess.BB_FILE_A,
    chess.BB_FILE_A | chess.BB_FILE_C,
    chess.BB_FILE_B | chess.BB_FILE_D,
    chess.BB_FILE_C | chess.BB_FILE_E,
    chess.BB_FILE_D | chess.BB_FILE_F,
    chess.BB_FILE_E | chess.BB_FILE_G,
    chess.BB_FILE_F | chess.BB_FILE_H,
    chess.BB_FILE_G
    ]

mop_up_values = {
    None    : 0,
    WPAWN   : 100,
    WBISHOP : 300,
    WKNIGHT : 300,
    WROOK   : 500,
    WQUEEN  : 900,
    WKING   : 0,
    BPAWN   : -100,
    BKNIGHT : -300,
    BBISHOP : -300,
    BROOK   : -500,
    BQUEEN  : -900,
    BKING   : -0
    }

def mop_up(board: chess.Board) -> int :

    material = [0, 0] # material score for [WHITE, BLACK]

    for square in chess.SquareSet(board.occupied) :

        value = mop_up_values[board.piece_at(square)]
        if value > 0 :
            material[0] += value
        else :
            material[1] -= value
    
    if material[0] == material[1] :
        return 0
    winner = 1
    if material[0] < material[1] :
        winner = -1
    
    return winner * (chess.square_distance(board.king(chess.WHITE if winner == 1 else chess.BLACK), chess.E4)
                      + 1.6 * (14 - chess.square_manhattan_distance(board.king(chess.WHITE), board.king(chess.BLACK))))

def evaluate(board: chess.Board) -> int :

    s2m = 1 if board.turn else -1

    late_eg = 0
    if chess.popcount(board.pawns) == 0 :
        late_eg = mop_up(board)

    score, phase, EG, MG = 0, 24, 0, 0

    w_pawns = board.pieces(chess.PAWN, chess.WHITE)
    b_pawns = board.pieces(chess.PAWN, chess.BLACK)

    for square in chess.SquareSet(board.occupied) :

        piece = board.piece_at(square)

        if piece is not None :

            phase -= VALUES[piece.piece_type][4]

            if piece.color == chess.WHITE :

                # Score + PSQT
                MG += VALUES[piece.piece_type][0][chess.SQUARES_180[square]] + VALUES[piece.piece_type][2]
                EG += VALUES[piece.piece_type][1][chess.SQUARES_180[square]] + VALUES[piece.piece_type][3]

                if piece.piece_type == chess.PAWN :

                    file_ = chess.square_file(square)
                    file_BB = chess.BB_FILES[file_]

                    # doubled pawns
                    if chess.popcount(int(w_pawns & file_BB)) >= 1 :
                        MG -= 5
                        EG -= 10

                    # isolated pawn
                    if int(w_pawns & ISOLATED_MASK[file_]) == 0 :
                        MG -= 5
                        EG -= 10

                elif piece.piece_type == chess.ROOK :

                    file_ = chess.BB_FILES[chess.square_file(square)]
                    
                    # semi-open files
                    if int(board.pieces(chess.PAWN, chess.WHITE) & file_) == 0 :
                        score += 10
                    
                    # open-files
                    if int(board.pawns & file_) == 0 :
                        score += 15

                # Bishop & Queen mobility
                elif piece.piece_type == chess.BISHOP :

                    score += 5 * (chess.popcount(int(board.attacks(square))) - 4)

                elif piece.piece_type == chess.QUEEN :

                    mb = chess.popcount(int(board.attacks(square))) - 9
                    MG += mb
                    EG += 2 * mb

                # King safety
                elif piece.piece_type == chess.KING :

                    file_ = chess.BB_FILES[chess.square_file(square)]
                    
                    # semi-open files
                    if int(board.pieces(chess.PAWN, chess.WHITE) & file_) == 0 :
                        score += 10
                    
                    # open-files
                    if int(board.pawns & file_) == 0 :
                        score += 15

                    score += 5 * chess.popcount(int(board.attacks(square) & board.occupied_co[chess.WHITE]))

            else : # Black

                # Score + PSQT
                MG -= VALUES[piece.piece_type][0][square] + VALUES[piece.piece_type][2]
                EG -= VALUES[piece.piece_type][1][square] + VALUES[piece.piece_type][3]

                if piece.piece_type == chess.PAWN :

                    file_ = chess.square_file(square)
                    file_BB = chess.BB_FILES[file_]

                    # doubled pawns
                    if chess.popcount(int(b_pawns & file_BB)) >= 1 :
                        MG += 5
                        EG += 10

                    # isolated pawn
                    if int(b_pawns & ISOLATED_MASK[file_]) == 0 :
                        MG += 5
                        EG += 10
                    
                elif piece.piece_type == chess.ROOK :

                    file_ = chess.BB_FILES[chess.square_file(square)]
                    
                    # semi-open files
                    if int(board.pieces(chess.PAWN, chess.BLACK) & file_) == 0 :
                        score -= 10
                    
                    # open-files
                    if int(board.pawns & file_) == 0 :
                        score -= 15

                # Bishop & Queen mobility
                elif piece.piece_type == chess.BISHOP :

                    score -= 5 * (chess.popcount(int(board.attacks(square))) - 4)

                elif piece.piece_type == chess.QUEEN :

                    mb = chess.popcount(int(board.attacks(square))) - 9
                    MG -= mb
                    EG -= 2 * mb

                # King safety
                elif piece.piece_type == chess.KING :

                    file_ = chess.BB_FILES[chess.square_file(square)]
                    
                    # semi-open files
                    if int(board.pieces(chess.PAWN, chess.BLACK) & file_) == 0 :
                        score += 10
                    
                    # open-files
                    if int(board.pawns & file_) == 0 :
                        score += 15

                    score += 5 * chess.popcount(int(board.attacks(square) & board.occupied_co[chess.BLACK]))
    
    # General positional eval

    # Minor pieces developed
    if board.piece_at(chess.B1) != WKNIGHT : MG += 8
    if board.piece_at(chess.C1) != WBISHOP : MG += 8
    if board.piece_at(chess.F1) != WBISHOP : MG += 8
    if board.piece_at(chess.G1) != WKNIGHT : MG += 8
    if board.piece_at(chess.B8) != BKNIGHT : MG -= 8
    if board.piece_at(chess.C8) != BBISHOP : MG -= 8
    if board.piece_at(chess.F8) != BBISHOP : MG -= 8
    if board.piece_at(chess.G8) != BKNIGHT : MG -= 8

    # Trapped bishop
    if board.piece_at(chess.A7) == WBISHOP  and  board.piece_at(chess.B6) == BPAWN : MG -= 120
    if board.piece_at(chess.H7) == WBISHOP  and  board.piece_at(chess.G6) == BPAWN : MG -= 120
    if board.piece_at(chess.A2) == BBISHOP  and  board.piece_at(chess.B3) == WPAWN : MG += 120
    if board.piece_at(chess.H2) == BBISHOP  and  board.piece_at(chess.G3) == WPAWN : MG += 120

    # Central pawn control
    if (board.piece_at(chess.E4) == WPAWN  or  board.piece_at(chess.E5) == WPAWN) and \
       (board.piece_at(chess.D4) == WPAWN  or  board.piece_at(chess.D5) == WPAWN) :
        MG += 15
    if (board.piece_at(chess.E4) == BPAWN  or  board.piece_at(chess.E5) == BPAWN) and \
       (board.piece_at(chess.D4) == BPAWN  or  board.piece_at(chess.D5) == BPAWN) :
        MG -= 15

    # Undevelopped central pawn
    if board.piece_at(chess.E2) == WPAWN  and  board.piece_at(chess.E3) != None : MG -= 15
    if board.piece_at(chess.D2) == WPAWN  and  board.piece_at(chess.D3) != None : MG -= 15
    if board.piece_at(chess.E7) == BPAWN  and  board.piece_at(chess.E6) != None : MG += 15
    if board.piece_at(chess.D7) == BPAWN  and  board.piece_at(chess.D6) != None : MG += 15
                
    # Tapered eval
    phase = (phase * 256 + 12) / 24
    score += ((MG * (256 - phase)) + (EG * phase)) / 256

    return skill(s2m * (score + late_eg))

def skill(value: float) -> int :
    if SKILL == 20 :
        return (int(value) // GRAIN) * GRAIN # faster this way
    return int(((value * SKILL) // (20 - SKILL + GRAIN)) * (20 - SKILL + GRAIN) / 20 + ((20 - SKILL) * random.random() * (SKILL - 20) * 200 - (SKILL - 20) * 100) / 20)