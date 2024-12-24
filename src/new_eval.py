import chess

# Evaluation constants

Infinity    = 32000
KingValue   = 10000
QueenValue  =   900
RookValue   =   500
BishopValue =   300
KnightValue =   300
PawnValue   =   100

RANK_1 = FILE_A = 0
RANK_2 = FILE_B = 1
RANK_3 = FILE_C = 2
RANK_4 = FILE_D = 3
RANK_5 = FILE_E = 4
RANK_6 = FILE_F = 5
RANK_7 = FILE_G = 6
RANK_8 = FILE_H = 7

WP = chess.Piece(chess.PAWN,   chess.WHITE)
WN = chess.Piece(chess.KNIGHT, chess.WHITE)
WB = chess.Piece(chess.BISHOP, chess.WHITE)
WR = chess.Piece(chess.ROOK,   chess.WHITE)
WQ = chess.Piece(chess.QUEEN,  chess.WHITE)
WK = chess.Piece(chess.KING,   chess.WHITE)
BP = chess.Piece(chess.PAWN,   chess.BLACK)
BN = chess.Piece(chess.KNIGHT, chess.BLACK)
BB = chess.Piece(chess.BISHOP, chess.BLACK)
BR = chess.Piece(chess.ROOK,   chess.BLACK)
BQ = chess.Piece(chess.QUEEN,  chess.BLACK)
BK = chess.Piece(chess.KING,   chess.BLACK)

# EndgameValue, MiddlegameValue:
# If the combined material score of pieces on both sides (excluding
# kings and pawns) is less than this value, we are in an endgame.
# If it is greater than MiddlegameValue, we use middlegame scoring.
# For anything in between, the score will be a weighted average of
# the middlegame and endgame scores.
EndgameValue    = 2400
MiddlegameValue = 4000

# Bonuses and penalties:

RookHalfOpenFile  =   8
RookOpenFile      =  20
RookPasserFile    =  25 # Rook on passed pawn file.
RookOnSeventh     =  25 # Rook on its 7th rank.
DoubledRooks      =  20 # Two rooks on same file.
RookEyesKing      =  12 # Attacks squares near enemy king.
KingTrapsRook     =  35 # E.g. King on f1, Rook on h1
DoubledPawn       =   8
IsolatedPawn      =  16
BackwardPawn      =  10 # Pawn at base of pawn chain.
# DispersedPawn     =  10  # Not in pawn chain/duo. (Unused)
BlockedHomePawn   =  15 # Blocked pawn on d2/e2/d7/e7.
BishopPair        =  25 # Pair of bishops.
BishopEyesKing    =  12 # Bishop targets enemy king.
BishopTrapped     = 120 # E.g. Bxa7? ...b6!
KnightOutpost     =  15 # 4th/5th/6th rank outpost.
KnightBadEndgame  =  30 # Enemy pawns on both wings.
BadPieceTrade     =  80 # Bad trade, e.g. minor for pawns.
CanCastle         =  10 # Bonus for castling rights.
Development       =   8 # Moved minor pieces in opening.
CentralPawnPair   =  15 # For d4/d5 + e4/e5 pawns.
CoverPawn         =  12 # Pawn cover for king.
PassedPawnRank = [
#   1   2   3   4   5   6    7  8th  rank
    0, 10, 15, 25, 50, 80, 120, 0
]

# Bishops (and rooks in endings) need to be mobile to be useful:
BishopMobility = [
#     0    1    2   3   4  5  6  7  8   9  10  11  12  13  14  15
    -20, -15, -10, -6, -3, 0, 3, 6, 9, 12, 15, 15, 15, 15, 15, 15
]
RookEndgameMobility = [
#     0    1    2    3   4  5  6  7  8  9 10 11 12 13 14 15
    -25, -20, -15, -10, -5, 2, 0, 2, 4, 6, 8, 8, 8, 8, 8, 8
]

# Piece distance to enemy king bonuses:    1   2   3   4   5   6   7
KnightKingDist = [ 0, 10, 14, 10,  5,  2,  0,  0 ]
BishopKingDist = [ 0,  8,  6,  4,  2,  1,  0,  0 ]
RookKingDist   = [ 0,  8,  6,  4,  2,  1,  0,  0 ]
QueenKingDist  = [ 0, 15, 12,  9,  6,  3,  0,  0 ]

# LazyEvalMargin
# A score that is further than this margin outside the current
# alpha-beta window after material evaluation is returned as-is.
# A larger margin is used for endgames (especially pawn endings)
# since positional bonuses can be much larger for them.'''
LazyEvalMargin           = 250
LazyEvalEndingMargin     = 400
LazyEvalPawnEndingMargin = 800

# PawnSquare:
# Gives bonuses to advanced pawns, especially in the centre.
PawnSquare = [
      0,   0,   0,   0,   0,   0,   0,   0, # A8 - H8
      4,   8,  12,  16,  16,  12,   8,   4,
      4,   8,  12,  16,  16,  12,   8,   4,
      3,   6,   9,  12,  12,   9,   6,   3,
      2,   4,   6,   8,   8,   6,   4,   2,
      1,   2,   3,   4,   4,   3,   2,   1,
      0,   0,   0,  -4,  -4,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0  # A1 - H1
]

# PawnStorm
# Bonus when side is castled queenside and opponent is
# castled kingside. Gives a bonus for own sheltering pawns
# and a penalty for pawns on the opposing wing to make them
# disposable and encourage them to move forwards.
PawnStorm = [
      0,   0,   0,   0,   0,   0,   0,   0, # A8 - H8
      0,   0,   0,   0,   2,   2,   2,   2,
      0,   0,   0,   0,   4,   2,   2,   2,
      0,   0,   0,   4,   6,   0,   0,   0,
      4,   4,   4,   4,   4,  -4,  -4,  -4,
      8,   8,   8,   0,   0,  -8,  -8,  -8,
     12,  12,  12,   0,   0, -12, -12, -12,
      0,   0,   0,   0,   0,   0,   0,   0  # A1 - H1
]

# KnightSquare
# Rewards well-placed knights.
KnightSquare = [
    -24, -12,  -6,  -6,  -6,  -6, -12, -24,
     -8,   0,   0,   0,   0,   0,   0,  -8,
     -6,   5,  10,  10,  10,  10,   5,  -6,
     -6,   0,  10,  10,  10,  10,   0,  -6,
     -6,   0,   5,   8,   8,   5,   0,  -6,
     -6,   0,   5,   5,   5,   5,   0,  -6,
     -6,   0,   0,   0,   0,   0,   0,  -8,
    -10,  -8,  -5,  -6,  -6,  -6,  -6, -10
]

# BishopSquare
# Bonus array for bishops.
BishopSquare = [
    -10,  -5,   0,   0,   0,   0,  -5, -10,
     -5,   8,   0,   5,   5,   0,   8,  -5,
      0,   0,   5,   5,   5,   5,   0,   0,
      0,   5,  10,   5,   5,  10,   5,   0,
      0,   5,  10,   5,   5,  10,   5,   0,
      0,   0,   5,   5,   5,   5,   0,   0,
     -5,   8,   0,   5,   5,   0,   8,  -5,
    -10,  -5,  -2,  -2,  -2,  -2,  -5, -10
]

# RookFile
# Bonus array for Rooks, by file.
#            a  b  c  d  e  f  g  h
RookFile = [ 0, 0, 4, 8, 8, 4, 0, 0 ]

# QueenSquare
# Bonus array for Queens.
QueenSquare = [
     -5,   0,   0,   0,   0,   0,   0,  -5, # A8 - H8
     -5,   0,   3,   3,   3,   3,   0,  -5,
      0,   3,   6,   9,   9,   6,   3,   0,
      0,   3,   9,  12,  12,   9,   3,   0,
     -5,   3,   9,  12,  12,   9,   3,  -5,
     -5,   3,   6,   9,   9,   6,   3,  -5,
     -5,   0,   3,   3,   3,   3,   0,  -5,
    -10,  -5,   0,   0,   0,   0,  -5, -10  # A1 - H1
]

# KingSquare
# Bonus array for kings in the opening and middlegame.
KingSquare = [
    -50, -50, -50, -50, -50, -50, -50, -50,
    -50, -50, -50, -50, -50, -50, -50, -50,
    -50, -50, -50, -50, -50, -50, -50, -50,
    -50, -50, -50, -60, -60, -50, -50, -50,
    -40, -40, -40, -60, -60, -40, -40, -40,
    -15, -15, -15, -20, -20, -15, -15, -15,
      5,   5,   0,   0,   0,   0,   5,   5,
     20,  20,  15,   5,   5,   5,  20,  20
]

# EndgameKingSquare
#  Rewards King centralisation in endgames.
KingEndgameSquare = [
    -10,  -5,   0,   5,   5,   0,  -5, -10,
     -5,   0,   5,  10,  10,   5,   0,  -5,
      0,   5,  10,  15,  15,  10,   5,   0,
      5,  10,  15,  20,  20,  15,  10,   5,
      5,  10,  15,  20,  20,  15,  10,   5,
      0,   5,  10,  15,  15,  10,   5,   0,
     -5,   0,   5,  10,  10,   5,   0,  -5,
    -10,  -5,   0,   5,   5,   0,  -5, -10
]

class PawnEntry :
    pawnhash = 0
    score = 0
    wLongbShortScore = 0
    wShortbLongScore = 0
    filePassers = [0, 0]

pawntable_size = 10_000
pawntable = [PawnEntry() for _ in range(pawntable_size)]

def is_outpost(board: chess.Board, square: chess.Square, color: chess.Color) -> bool :

    enemy_pawn = chess.Piece(chess.PAWN, not color)
    rank = chess.square_rank(square)

    if color == chess.WHITE :
        if rank < RANK_4 or rank > RANK_6 :
            return False
    else :
        if rank < RANK_3 or rank > RANK_5 :
            return False

    for square in board.attackers(not color, square) :
        if board.piece_at(square) == enemy_pawn :
            return False
    return True

def white_material(board: chess.Board) -> int :
    return chess.popcount(board.queens  & board.occupied_co[chess.WHITE]) * QueenValue  \
         + chess.popcount(board.rooks   & board.occupied_co[chess.WHITE]) * RookValue   \
         + chess.popcount(board.bishops & board.occupied_co[chess.WHITE]) * BishopValue \
         + chess.popcount(board.knights & board.occupied_co[chess.WHITE]) * KnightValue \
         + chess.popcount(board.pawns   & board.occupied_co[chess.WHITE]) * PawnValue

def black_material(board: chess.Board) -> int :
    return chess.popcount(board.queens  & board.occupied_co[chess.BLACK]) * QueenValue  \
         + chess.popcount(board.rooks   & board.occupied_co[chess.BLACK]) * RookValue   \
         + chess.popcount(board.bishops & board.occupied_co[chess.BLACK]) * BishopValue \
         + chess.popcount(board.knights & board.occupied_co[chess.BLACK]) * KnightValue \
         + chess.popcount(board.pawns   & board.occupied_co[chess.BLACK]) * PawnValue

def material_value(board: chess.Board) -> int :
    s = white_material(board) - black_material(board)
    return s if board.turn else -s
         
def score(board: chess.Board, alpha: int=-Infinity, beta: int=Infinity) -> int :

    piece_count   = {
        WP : chess.popcount(board.occupied_co[chess.WHITE] & board.pawns),
        WN : chess.popcount(board.occupied_co[chess.WHITE] & board.knights),
        WB : chess.popcount(board.occupied_co[chess.WHITE] & board.bishops),
        WR : chess.popcount(board.occupied_co[chess.WHITE] & board.rooks),
        WQ : chess.popcount(board.occupied_co[chess.WHITE] & board.queens),
        BP : chess.popcount(board.occupied_co[chess.BLACK] & board.pawns),
        BN : chess.popcount(board.occupied_co[chess.BLACK] & board.knights),
        BB : chess.popcount(board.occupied_co[chess.BLACK] & board.bishops),
        BR : chess.popcount(board.occupied_co[chess.BLACK] & board.rooks),
        BQ : chess.popcount(board.occupied_co[chess.BLACK] & board.queens)
    }
    materialScore = [0, 0]
    allscore      = [0, 0] # Scoring in all positions
    endscore      = [0, 0] # Scoring in endgames
    midscore      = [0, 0] # Scoring in middlegames
    nNonPawns     = [0, 0] # Non-pawns on each side, including kings

    nNonPawns[chess.WHITE] = chess.popcount(board.occupied_co[chess.WHITE]) - piece_count[WP]
    nNonPawns[chess.BLACK] = chess.popcount(board.occupied_co[chess.BLACK]) - piece_count[BP]

    # First compute material scores
    allscore[chess.WHITE] = materialScore[chess.WHITE] = white_material(board)
    allscore[chess.BLACK] = materialScore[chess.BLACK] = black_material(board)

    pieceMaterial = (materialScore[chess.WHITE] - piece_count[WP] * PawnValue) \
                  + (materialScore[chess.BLACK] - piece_count[BP] * PawnValue)
    
    inEndgame = False
    inMiddlegame = False

    if pieceMaterial <= EndgameValue :
        inEndgame = True
    if pieceMaterial >= MiddlegameValue :
        inMiddlegame = True
    inPawnEndgame = (board.occupied == (board.pawns & board.kings))

    # Look for a bad trade: minor piece for pawns Q for R+Pawns etc.
    # But only do this if both sides have pawns.
    if chess.popcount(board.occupied_co[chess.WHITE] & board.pawns) > 0 and chess.popcount(board.occupied_co[chess.BLACK]) > 0 :
        wminors = piece_count[WB] + piece_count[WN]
        bminors = piece_count[BB] + piece_count[BN]
        wmajors = piece_count[WR] + (2 * piece_count[WQ])
        bmajors = piece_count[BR] + (2 * piece_count[BQ])
        if wmajors == bmajors :
            if wminors < bminors :
                allscore[chess.WHITE] -= BadPieceTrade
            if wminors > bminors :
                 allscore[chess.BLACK] -= BadPieceTrade
        elif wminors == bminors :
            if wmajors < bmajors :
                allscore[chess.WHITE] -= BadPieceTrade
            if wmajors > bmajors :
                allscore[chess.BLACK] -= BadPieceTrade

    # Add the Bishop-pair bonus now, because it is fast and easy:
    if (piece_count[WB] >= 2) : allscore[chess.WHITE] += BishopPair
    if (piece_count[BB] >= 2) : allscore[chess.BLACK] += BishopPair

    # If there are no pawns, a material advantage of only one minor
    # piece is worth very little so reduce the material score.
    if not board.pawns :
        materialDiff = materialScore[chess.WHITE] - materialScore[chess.BLACK]
        if materialDiff < 0 : materialDiff = -materialDiff
        if materialDiff == BishopValue or materialDiff == KnightValue :
            allscore[chess.WHITE] /= 4
            allscore[chess.BLACK] /= 4

    # Look for a trapped bishop on a7/h7/a2/h2
    if board.piece_at(chess.A7) == WB and board.piece_at(chess.B6) == BP : allscore[chess.WHITE] -= BishopTrapped
    if board.piece_at(chess.H7) == WB and board.piece_at(chess.G6) == BP : allscore[chess.WHITE] -= BishopTrapped
    if board.piece_at(chess.A2) == BB and board.piece_at(chess.B3) == WP : allscore[chess.BLACK] -= BishopTrapped
    if board.piece_at(chess.H2) == BB and board.piece_at(chess.G6) == WP : allscore[chess.BLACK] -= BishopTrapped

    # Check for a score much worse than alpha or better than beta
    # which can be returned immediately on the assumption that
    # a full evaluation could not get inside the alpha-beta range.
    # If we are in a pawn ending, a much larger margin is used since
    # huge bonuses can be added for passed pawns in such endgames.
    lazyMargin = LazyEvalMargin
    if inEndgame : lazyMargin = LazyEvalEndingMargin
    if inPawnEndgame :lazyMargin = LazyEvalPawnEndingMargin

    fastScore = allscore[chess.WHITE] - allscore[chess.BLACK]
    if not board.turn : fastScore = -fastScore
    if fastScore - lazyMargin > beta  : return int(fastScore)
    if fastScore + lazyMargin < alpha : return int(fastScore)

    # Get the pawn structure score next, because it is usually fast
    pawn_entry = score_pawn(board)

    # Penalise d-file and e-file pawns blocked on their home squares
    if board.piece_at(chess.D2) == WP and board.piece_at(chess.D3) != None : allscore[chess.WHITE] -= BlockedHomePawn
    if board.piece_at(chess.E2) == WP and board.piece_at(chess.E3) != None : allscore[chess.WHITE] -= BlockedHomePawn
    if board.piece_at(chess.D7) == BP and board.piece_at(chess.D6) != None : allscore[chess.BLACK] -= BlockedHomePawn
    if board.piece_at(chess.E7) == BP and board.piece_at(chess.E6) != None : allscore[chess.BLACK] -= BlockedHomePawn

    # Incentive for side ahead in material to trade nonpawn pieces and
    # for side behind in material to avoid trades
    if materialScore[chess.WHITE] > materialScore[chess.BLACK] :
        bonus = (5 - nNonPawns[chess.BLACK]) * 5
        allscore[chess.WHITE] += bonus
    elif materialScore[chess.BLACK] > materialScore[chess.WHITE] :
        bonus = (5 - nNonPawns[chess.WHITE]) * 5
        allscore[chess.BLACK] += bonus

    # Check again for a score outside the alpha-beta range, using a
    # smaller fixed margin of error since the pawn structure score
    # has been added
    fastScore = allscore[chess.WHITE] - allscore[chess.BLACK] + pawn_entry.score
    if not board.turn : fastScore = -fastScore
    if fastScore > beta + 200 : return int(fastScore)
    if fastScore < alpha - 200 : return int(fastScore)

    # Now refine the score with piece-square bonuses

    wk = board.king(chess.WHITE)
    bk = board.king(chess.BLACK)
    wkfile = chess.square_file(wk)
    bkfile = chess.square_file(bk)

    # Check if each side should be storming the enemy king
    if not inEndgame :
        if wkfile <= FILE_C and bkfile >= FILE_F :
            midscore[chess.WHITE] += pawn_entry.wLongbShortScore
        elif wkfile >= FILE_F and bkfile <= FILE_C :
            midscore[chess.WHITE] += pawn_entry.wShortbLongScore
    
    # Iterate over the piece for each color
    for color in chess.COLORS :
        enemy = not color
        enemyKing = board.king(enemy)
        mscore = 0 # Middlegame score adjustments
        escore = 0 # Endgame score adjustments
        ascore = 0 # All-position adjustments (middle and endgame)

        for sq in chess.SquareSet(board.occupied_co[color]) :
            p = board.piece_at(sq)
            ptype = p.piece_type
            bonusSq = sq if color == chess.WHITE else chess.square_mirror(sq)
            rank = RANK_1 + RANK_8 - chess.square_rank(bonusSq)

            # Piece-specific bonuses
            if ptype == chess.PAWN :
                # Most pawn-specific bonuses are in score_pawn

                # Kings should be close to pawns in endgames
                if not inMiddlegame :
                    escore += 3 * chess.square_distance(sq, enemyKing) \
                             - 2 * chess.square_distance(sq, board.king(color))
                
            elif ptype == chess.ROOK :
                ascore += RookFile[chess.square_file(sq)]
                if rank == RANK_7 :
                    ascore += RookOnSeventh
                    # Even bigger bonus if rook traps king on 8th rank
                    kingOn8th = (bk >= chess.A8) if p == WR else (wk <= chess.H1)
                    if kingOn8th : ascore += RookOnSeventh
                if not inEndgame :
                    mscore += RookKingDist[chess.square_distance(sq, enemyKing)]
                if not inMiddlegame :
                    mobility = chess.popcount(int(board.attacks(sq)))
                    escore += RookEndgameMobility[mobility]
            
            elif ptype == chess.KING :
                if chess.popcount(board.occupied_co[color]) == 1 :
                    # Forcing a lone king to a corner
                    ascore += 5 * KingEndgameSquare[bonusSq] - 150
                else :
                    mscore += KingSquare[bonusSq]
                    escore += KingEndgameSquare[bonusSq]
            
            elif ptype == chess.BISHOP :
                ascore += BishopSquare[bonusSq]
                ascore += BishopMobility[chess.popcount(int(board.attacks(sq)))]
                # Middlegame bonus for diagonal close to enemy king
                if not inEndgame :
                    mscore += BishopKingDist[chess.square_distance(sq, enemyKing)]
                    # TODO : Reward a bishop attacking the enemy king vicinity
                    # leftdiff = square_LeftDiag(sq) - square_LeftDiag(enemyKing)
                    # rightdiff = square_RightDiag(sq) - square_RightDiag(enemyKing)
                    # if (leftdiff >= -2 and leftdiff <= 2) \
                    #      or  (rightdiff >= -2 and rightdiff <= 2) :
                    #    mscore += BishopEyesKing

            elif ptype == chess.KNIGHT :
                ascore += KnightSquare[bonusSq]
                if not inEndgame :
                    mscore += KnightKingDist[chess.square_distance(sq, enemyKing)]
                    # Bonus for a useful outpost
                    # TODO : and not is edge square
                    if rank >= RANK_4 and is_outpost(board, sq, color) :
                        mscore += KnightOutpost
                if not inMiddlegame :
                    # Penalty for knight in an endgame with enemy
                    # pawns on both wings.
                    qsidePawns = chess.popcount(board.occupied_co[enemy] & board.pawns & chess.BB_FILE_A & chess.BB_FILE_B & chess.BB_FILE_C)
                    ksidePawns = chess.popcount(board.occupied_co[enemy] & board.pawns & chess.BB_FILE_F & chess.BB_FILE_G & chess.BB_FILE_H)
                    if ksidePawns > 0 and qsidePawns > 0 :
                        escore -= KnightBadEndgame
            
            elif ptype == chess.QUEEN :
                ascore += QueenSquare[bonusSq]
                ascore += QueenKingDist[chess.square_distance(sq, enemyKing)]

        allscore[color] += ascore
        midscore[color] += mscore
        endscore[color] += escore

    # Now reward rooks on open files or behind passed pawns
    passedPawnfiles = pawn_entry.filePassers[chess.WHITE] | pawn_entry.filePassers[chess.BLACK]
    for color in chess.COLORS :
        rook = WR if color == chess.WHITE else BR
        if piece_count[rook] == 0 : continue
        enemy = not color
        enemyKingfile = chess.square_file(board.king(enemy))
        bonus = 0

        for file in chess.BB_FILES :
            nRooks = chess.popcount(board.rooks & file & board.occupied_co[color])
            if nRooks == 0 : continue
            if nRooks > 1 : bonus += DoubledRooks
            passedPawnsOnfile = passedPawnfiles & file
            if passedPawnsOnfile != 0 :
                # Rook is on same file as a passed pawn.
                bonus += RookPasserFile
            elif chess.popcount(file & board.pawns & board.occupied_co[color]) == 0 :
                # Rook on open or half-open file
                if chess.popcount(file & board.pawns & board.occupied_co[enemy]) == 0 :
                    bonus += RookOpenFile
                else :
                    bonus += RookHalfOpenFile
                # If this open/half-open file leads to a square adjacent
                # to the enemy king, give a further bonus:
                fdiff = abs(chess.BB_FILES.index(file) - enemyKingfile)
                if fdiff >= -1 and fdiff < 1 : bonus += RookEyesKing
        allscore[color] += bonus

    # King safety
    if not inEndgame :
        if wk in (chess.B1, chess.C1, chess.G1) : midscore[chess.WHITE] += 2*CanCastle + 5
        if bk in (chess.B8, chess.C8, chess.G8) : midscore[chess.WHITE] += 2*CanCastle + 5
        if piece_count[BQ] > 0 :
            if board.castling_rights & chess.BB_H1 : midscore[chess.WHITE] += CanCastle
            if board.castling_rights & chess.BB_A1 : midscore[chess.WHITE] += CanCastle
        if piece_count[WQ] > 0 :
            if board.castling_rights & chess.BB_H8 : midscore[chess.BLACK] += CanCastle
            if board.castling_rights & chess.BB_A8 : midscore[chess.BLACK] += CanCastle
        # Bonus for pawn cover in front of a castled king. Actually we
        # also include bishops because they are important for defence.
        if chess.square_rank(wk) == RANK_1 and wk != chess.D1 and wk != chess.E1 :
            nCoverPawns = chess.popcount(int(board.attacks(wk)) & board.occupied_co[chess.WHITE] & board.pawns & board.bishops)
            midscore[chess.WHITE] += CoverPawn * nCoverPawns
            if (wk == chess.F1 or wk == chess.G1) \
                 and (board.piece_at(chess.G1) == WR or board.piece_at(chess.H1) == WR or board.piece_at(chess.H2) == WR) :
                midscore[chess.WHITE] -= KingTrapsRook
            if (wk == chess.C1 or wk == chess.B1) \
                 and (board.piece_at(chess.B1) == WR or board.piece_at(chess.A1) == WR or board.piece_at(chess.A2) == WR) :
                midscore[chess.WHITE] -= KingTrapsRook
        if chess.square_rank(bk) == RANK_1 and wk != chess.D8 and wk != chess.E8 :
            nCoverPawns = chess.popcount(int(board.attacks(bk)) & board.occupied_co[chess.BLACK] & board.pawns & board.bishops)
            midscore[chess.BLACK] += CoverPawn * nCoverPawns
            if (bk == chess.F8 or bk == chess.G8) \
                 and (board.piece_at(chess.G8) == BR or board.piece_at(chess.H8) == BR or board.piece_at(chess.H7) == BR) :
                midscore[chess.BLACK] -= KingTrapsRook
            if (bk == chess.C8 or bk == chess.B8) \
                 and (board.piece_at(chess.B8) == BR or board.piece_at(chess.A8) == BR or board.piece_at(chess.A7) == BR) :
                midscore[chess.BLACK] -= KingTrapsRook

        # Pawn centre:
        if (board.piece_at(chess.D4) == WP or board.piece_at(chess.D5) == WP) \
               and (board.piece_at(chess.E4) == WP or board.piece_at(chess.E5) == WP) :
            midscore[chess.WHITE] += CentralPawnPair
        if (board.piece_at(chess.D4) == BP or board.piece_at(chess.D5) == BP) \
                and (board.piece_at(chess.E4) == BP or board.piece_at(chess.E5) == BP) :
            midscore[chess.BLACK] += CentralPawnPair

        # Minor pieces developed:
        if board.piece_at(chess.B1) != WN : midscore[chess.WHITE] += Development
        if board.piece_at(chess.C1) != WB : midscore[chess.WHITE] += Development
        if board.piece_at(chess.F1) != WB : midscore[chess.WHITE] += Development
        if board.piece_at(chess.G1) != WN : midscore[chess.WHITE] += Development
        if board.piece_at(chess.B8) != BN : midscore[chess.BLACK] += Development
        if board.piece_at(chess.C8) != BB : midscore[chess.BLACK] += Development
        if board.piece_at(chess.F8) != BB : midscore[chess.BLACK] += Development
        if board.piece_at(chess.G8) != BN : midscore[chess.BLACK] += Development

    # Work out the middlegame and endgame scores including pawn structure
    # evaluation, with a larger pawn structure weight in endgames:
    baseScore = allscore[chess.WHITE] - allscore[chess.BLACK]
    mgScore = baseScore + midscore[chess.WHITE] - midscore[chess.BLACK]
    egScore = baseScore + endscore[chess.WHITE] - endscore[chess.BLACK]
    mgScore += pawn_entry.score
    egScore += (pawn_entry.score * 5) / 4

    # Scale down the endgame score for bishops of opposite colors, if both
    # sides have the same non-pawn material:
    if piece_count[WB] == 1 and piece_count[BB] == 1 :
        if chess.popcount(board.occupied_co[chess.WHITE] & board.bishops & chess.BB_LIGHT_SQUARES) != chess.popcount(board.occupied_co[chess.BLACK] & board.bishops & chess.BB_LIGHT_SQUARES) :
            if piece_count[WQ] == piece_count[BQ] \
                  and piece_count[WR] == piece_count[BR] \
                  and piece_count[WN] == piece_count[BN] :
                egScore = egScore * 5 / 8

    # Negate scores for Black to move:
    if not board.turn :
        mgScore = -mgScore
        egScore = -egScore

    # Determine the final score from the middlegame and endgame scores:
    finalScore = 0
    if inMiddlegame :
        finalScore = mgScore # Use the middlegame score only.
    elif inEndgame :
        finalScore = egScore # Use the endgame score only.
    else :
        # The final score is a weighted mean of the two scores:
        midpart = (pieceMaterial - EndgameValue) * mgScore
        endpart = (MiddlegameValue - pieceMaterial) * egScore
        finalScore = (endpart + midpart) / (MiddlegameValue - EndgameValue)
    return int(finalScore)

def score_pawn(board: chess.Board) -> PawnEntry :
    entry = PawnEntry()

    inPawnEndgame = (chess.popcount(board.occupied) - chess.popcount(board.pawns) == 2)

    if not inPawnEndgame :
        hashf = hash((board.occupied_co[chess.WHITE] & board.pawns, board.occupied_co[chess.BLACK] & board.pawns))
        e = pawntable[hashf % pawntable_size]
        if e.pawnhash == hashf :
            return e

    # The pawnFiles array contains the number of pawns of each color on
    # each file. Indexes 1-8 are used while 0 and 9 are empty dummy files
    # added so that even the a and h files have two adjacent files, making
    # isolated/passed pawn calculation easier.
    pawnFiles = [ [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ]
    # firstRank stores the rank of the leading pawn on each file.
    firstRank = [ [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ]
    # lastRank stores the rank of the rearmost pawn on each file.
    lastRank  = [ [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                  [7, 7, 7, 7, 7, 7, 7, 7, 7, 7] ]
    pawnScore = [0, 0]
    longVsShortScore = [0, 0] # Pawn storm bonuses, O-O-O vs O-O
    shortVsLongScore = [0, 0] # Pawn storm bonuses, O-O vs O-O-O
    bestRacingPawn = [RANK_1, RANK_1]

    for f_id in range(len(chess.BB_FILES)) :
        pawnFiles[chess.WHITE][f_id+1] = chess.popcount(board.occupied_co[chess.WHITE] & board.pawns & chess.BB_FILES[f_id])
        pawnFiles[chess.BLACK][f_id+1] = chess.popcount(board.occupied_co[chess.BLACK] & board.pawns & chess.BB_FILES[f_id])

    for color in chess.COLORS :
        for sq in chess.SquareSet(board.occupied_co[color] & board.pawns) :
            wsq = sq if color == chess.WHITE else chess.square_mirror(sq)
            bonusSq = chess.square_mirror(wsq)
            pawnScore[color] += PawnSquare[bonusSq]
            longVsShortScore[color] += PawnStorm[bonusSq]
            shortVsLongScore[color] += PawnStorm[chess.square_mirror(bonusSq)]
            file = chess.square_file(wsq) + 1
            rank = chess.square_rank(wsq)
            if rank > firstRank[color][file] :
                firstRank[color][file] = rank
            if rank < lastRank[color][file] :
                lastRank[color][file] = rank

    fileHasPassers = [0, 0]

    for color in chess.COLORS :
        if chess.popcount(board.occupied_co[color] & board.pawns) == 0 : continue
        enemy = not color
        
        for file in range(len(chess.FILE_NAMES)) :
            pawnCount = pawnFiles[color][file]
            if pawnCount == 0 : continue
            pawnRank = firstRank[color][file]

            # Doubled pawn penalty
            if pawnCount > 1 :
                pawnScore[color] -= DoubledPawn * pawnCount

            # Isolated pawn penalty
            isolated = False
            if pawnFiles[color][file-1] == 0 and  pawnFiles[color][file+1] == 0 :
                isolated = True
                pawnScore[color] -= IsolatedPawn * pawnCount
                # Extra penalty for isolated on half-open file
                if pawnFiles[enemy][file] == 0 :
                    pawnScore[color] -= IsolatedPawn * pawnCount / 2
            elif lastRank[color][file-1] > lastRank[color][file] \
                   and  lastRank[color][file+1] > lastRank[color][file] :
                # Not isolated, but backward
                pawnScore[color] -= BackwardPawn
                # Extra penalty for backward on half-open file
                if pawnFiles[enemy][file] == 0 :
                    pawnScore[color] -= BackwardPawn

            # Passed pawn bonus:
            if pawnRank >= 7 - lastRank[enemy][file] \
                  and pawnRank >= 7 - lastRank[enemy][file-1] \
                  and pawnRank >= 7 - lastRank[enemy][file+1] :
                bonus = PassedPawnRank[pawnRank]
                # Smaller bonus for rook-file or isolated passed pawns
                if file == 1 or file == 8 or isolated :
                    bonus = bonus * 3 / 4
                # Bigger bonus for a passed pawn protected by another pawn
                if not isolated :
                    if (pawnRank == firstRank[color][file-1] + 1 
                          or pawnRank == firstRank[color][file+1] + 1) :
                        bonus = (bonus * 3) / 2
                pawnScore[color] += bonus
                # Update the passed-pawn-files bitmap
                fileHasPassers[color] |= (1 << (file-1))

                # Give a big bonus for a connected passed pawn on
                # the 6th or 7th rank.
                if (pawnRank >= RANK_6  and  pawnFiles[color][file-1] > 0
                      and  firstRank[color][file-1] >= RANK_6) :
                    # pawnScore[color] += some_bonus...
                    pass
                
                # Check for passed pawn races in pawn endgames
                if inPawnEndgame :
                    # Check if the enemy king is outside the square
                    kingSq = board.king(not color)
                    pawnSq = chess.square(file-1, pawnRank)
                    promoSq = chess.square(file-1, RANK_8)
                    if color == chess.BLACK :
                        pawnSq = chess.square_mirror(pawnSq)
                        promoSq = chess.square_mirror(promoSq)
                    kingDist = chess.square_distance(kingSq, promoSq)
                    pawnDist = chess.square_distance(pawnSq, promoSq)
                    if color != board.turn : pawnDist += 1
                    if pawnDist < kingDist :
                        bestRacingPawn[color] = pawnRank

    score = pawnScore[chess.WHITE] - pawnScore[chess.BLACK]
    entry.score = score
    entry.filePassers[chess.WHITE] = fileHasPassers[chess.WHITE]
    entry.filePassers[chess.BLACK] = fileHasPassers[chess.BLACK]
    entry.wLongbShortScore = longVsShortScore[chess.WHITE] - shortVsLongScore[chess.BLACK]
    entry.wShortbLongScore = shortVsLongScore[chess.WHITE] - longVsShortScore[chess.BLACK]

    if not inPawnEndgame :
        #global pawntable
        entry.pawnhash = hash((board.occupied_co[chess.WHITE] & board.pawns, board.occupied_co[chess.BLACK] & board.pawns))
        pawntable[hashf % pawntable_size] = entry
        return entry
    
    if bestRacingPawn[chess.WHITE] > bestRacingPawn[chess.BLACK] + 1 :
        entry.score += RookValue
    elif bestRacingPawn[chess.BLACK] > bestRacingPawn[chess.WHITE] + 1 :
        entry.score -= RookValue

    return entry