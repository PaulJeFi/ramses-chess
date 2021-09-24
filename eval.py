import chess
import copy

infinity = float('inf')

# Next, from A1 to H8 -> ^ ->

# Toutes les probabilités de position pour chaque pièce.
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

K.reverse()
K_end.reverse()
Q.reverse()
R.reverse()
N.reverse()
B.reverse()
P.reverse()

def minuscule(liste) :
    var = copy.deepcopy(liste)
    var.reverse()
    new_var = []
    for i in var :
        new_var.append(-i)
    return new_var

k, k_end, q, r, n, b, p = minuscule(K), minuscule(K_end), minuscule(Q), minuscule(R), minuscule(N), minuscule(B), minuscule(P)

PawnPhase = 0
KnightPhase = 1
BishopPhase = 1
RookPhase = 2
QueenPhase = 4
TotalPhase = PawnPhase*16 + KnightPhase*4 + BishopPhase*4 + RookPhase*4 + QueenPhase*2

def phase(pos) :
    '''Détermine la phase de jeu.'''
    '''Définit la phase d'une posiotion.'''
    
    phase = TotalPhase

    phase -= number(pos, 'P') * PawnPhase #// Where wp is the number of white pawns currently on the board
    phase -= number(pos, 'N') * KnightPhase    #// White knights
    phase -= number(pos, 'B') * BishopPhase
    phase -= number(pos, 'R') * RookPhase
    phase -= number(pos, 'Q') * QueenPhase
    phase -= number(pos, 'p') * PawnPhase
    phase -= number(pos, 'n') * KnightPhase
    phase -= number(pos, 'b') * BishopPhase
    phase -= number(pos, 'r') * RookPhase
    phase -= number(pos, 'q') * QueenPhase

    phase = (phase * 256 + (TotalPhase / 2)) / TotalPhase
    if phase > 80 :
        Phase = 'Fin de partie'
    elif phase > 20 :
        Phase = "Milieu de jeu"
    else :
        Phase = 'Ouverture'
    return Phase
    
def number(pos, Piece) :
    '''Nombre de Piece sur l'échiquier.'''
    nombre = 0
    for case in list(chess.SQUARES) :
        piece = pos.piece_at(case)
        if piece != None :
            if piece.symbol() == Piece :
                nombre = nombre + 1
    return nombre

def rook_knight_value(pos) :
    '''Valeur des pièces selon le nombre de pions restants.'''
    pawn_number = 0
    for case in list(chess.SQUARES) :
        piece = pos.piece_at(case)
        if piece != None :
            if piece.symbol() == 'P' or piece.symbol() == 'p' :
                pawn_number = pawn_number + 1
    rook = 5 + (1 - pawn_number/16)
    knight = 3 - (1 - pawn_number/16)/3
    return (rook, knight)

def placement_eval(pos) :
    '''"Évaluation du placement des pièces.'''
    if phase(pos) == 'Fin de partie' :
        # Référence aux listes selon les pièces.
        pieces = {'K': K_end, 'k': k_end, 'Q': Q, 'q': q, 'R': R, 'r': r, 'N': N, 'n': n, 'B': B, 'b': b, 'P': P, 'p': p}
    else :
        # Référence aux listes selon les pièces.
        pieces = {'K': K, 'k': k, 'Q': Q, 'q': q, 'R': R, 'r': r, 'N': N, 'n': n, 'B': B, 'b': b, 'P': P, 'p': p}
    evalu = 0
    for case in list(chess.SQUARES) :
        piece = pos.piece_at(case)
        if piece != None :
            evalu = evalu + pieces[piece.symbol()][case]/10
    return evalu / 15

def piece_list(pos) :
    '''Renvoie la liste des pièces présentes sur l'échiquier.'''
    piece_liste = []
    for place in chess.SQUARES :
        if pos.piece_at(place) != None :
            piece_liste.append(pos.piece_at(place).symbol())
    return piece_liste

def game_is_finished(pos) :
    '''Détermine si la partie est finie.'''
    if pos.is_checkmate() or pos.is_stalemate() or pos.is_insufficient_material() or pos.can_claim_threefold_repetition() :
        return True
    else :
        return False

def attack_protect(pos) :
    '''Évalue les pièces attaquées et défendues.'''
    values = {'K': -infinity, 'k': infinity, 'Q': -9, 'q': 9, 'R': -rook_knight_value(pos)[0], 'r': rook_knight_value(pos)[0], 'N': -rook_knight_value(pos)[1], 'n': rook_knight_value(pos)[1], 'B': -3, 'b': 3, 'P': -1, 'p': 1}
    squares = []
    liste = {True: 'QRNBP', False: 'qrnbp'}
    for place in chess.SQUARES :
        if pos.piece_at(place) != None :
            squares.append(place)
    evalu = 0
    for square in squares :
        square_eval = 0
        if len(pos.attackers(not pos.turn, square)) !=0 and pos.piece_at(square).symbol() in liste[pos.turn] :
            square_eval = (len(list(pos.attackers(chess.WHITE, square))) - len(list(pos.attackers(chess.BLACK, square)))) * (0.5 * values[pos.piece_at(square).symbol()])
            evalu = evalu + square_eval
    return evalu

# Les MailBox seront utilisées pour le sécurité du roi et les structures de pions.
pre_mailbox = [
     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
     -1,  0,  1,  2,  3,  4,  5,  6,  7, -1,
     -1,  8,  9, 10, 11, 12, 13, 14, 15, -1,
     -1, 16, 17, 18, 19, 20, 21, 22, 23, -1,
     -1, 24, 25, 26, 27, 28, 29, 30, 31, -1,
     -1, 32, 33, 34, 35, 36, 37, 38, 39, -1,
     -1, 40, 41, 42, 43, 44, 45, 46, 47, -1,
     -1, 48, 49, 50, 51, 52, 53, 54, 55, -1,
     -1, 56, 57, 58, 59, 60, 61, 62, 63, -1,
     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1
]

pre_mailbox64 = [
    21, 22, 23, 24, 25, 26, 27, 28,
    31, 32, 33, 34, 35, 36, 37, 38,
    41, 42, 43, 44, 45, 46, 47, 48,
    51, 52, 53, 54, 55, 56, 57, 58,
    61, 62, 63, 64, 65, 66, 67, 68,
    71, 72, 73, 74, 75, 76, 77, 78,
    81, 82, 83, 84, 85, 86, 87, 88,
    91, 92, 93, 94, 95, 96, 97, 98
]

mailbox = []
for i in range(len(pre_mailbox)) :
    mailbox.append(pre_mailbox[(len(pre_mailbox)-1)-i])
mailbox64 = []
for i in range(len(pre_mailbox64)) :
    mailbox64.append(pre_mailbox64[(len(pre_mailbox64)-1)-i])

def found_king(board, color) :
    '''Trouve l'emplacement du roi de couleur donnée.'''
    if color == chess.WHITE :
        king = 'K'
    else :
        king = 'k'
    for place in chess.SQUARES :
        if board.piece_at(place) != None :
            if board.piece_at(place).symbol() == king :
                return place

def next_to_king(board, king) :
    vector = [-11, -10, -9, -1, 0, 1, 9, 10, 11]
    next_to = []
    for dep in vector :
        if mailbox[mailbox64[king]-dep] != -1 :
            next_to.append(mailbox64.index(mailbox64[king]-dep))
    return next_to

def king_safety(board) :
    '''Évalue la sécurité des rois.'''
    safety = 0
    King = found_king(board, chess.WHITE)
    king = found_king(board, chess.BLACK)
    next_K = next_to_king(board, King)
    next_k = next_to_king(board, king)
    for square in next_K :
        safety = safety - len(list(board.attackers(chess.BLACK, square)))
    for square in next_k :
        safety = safety + len(list(board.attackers(chess.WHITE, square)))
    return safety

def quiesce(pos, alpha, beta) :
    '''Effecture une recherche de quiescence.'''
    stand_pat = materiel_eval(pos)
    if stand_pat >= beta :
        return beta
    if alpha < stand_pat:
        alpha = stand_pat
    for move in pos.legal_moves :
        if pos.is_capture(move) :
            pos.push(move)        
            score = -quiesce(pos, -beta, -alpha)
            pos.pop()
            if score >= beta :
                return beta
            if score > alpha :
                alpha = score  
    return alpha - materiel_eval(pos)

def materiel_eval(pos) :
    '''Evaluation matérielle.'''
    piece_liste = piece_list(pos)
    evaluation = 0
    for i in piece_liste :
        if i == 'Q' :
            evaluation = evaluation + 9
        elif i == 'q' :
            evaluation = evaluation - 9
        elif i == 'R' :
            evaluation = evaluation + rook_knight_value(pos)[0]
        elif i == 'r' :
            evaluation = evaluation - rook_knight_value(pos)[0]
        elif i == 'N' :
            evaluation = evaluation + rook_knight_value(pos)[1]
        elif i == 'n' :
            evaluation = evaluation - rook_knight_value(pos)[1]
        elif i == 'B' :
            evaluation = evaluation + 3
        elif i == 'b' :
            evaluation = evaluation - 3
        elif i == 'P' :
            evaluation = evaluation + 1
        elif i == 'p' :
            evaluation = evaluation - 1
    return evaluation

def mobility_eval(pos) :
    '''Evalue la mobilité des pièces.'''
    evaluation = 0
    opponent_legal_moves = []
    current_player_legal_moves = [move for move in pos.legal_moves]

    for i in range(len(current_player_legal_moves)-1) :
        pos.push_san(str(current_player_legal_moves[i]))
        opponent_legal_moves.append(pos.legal_moves.count())
        if pos.is_checkmate() :
            pos.pop()
            return (-1+2*pos.turn) * infinity
        elif game_is_finished(pos) :
            pos.pop()
            return 0
        pos.pop()
    moyenne = 0
    for i in opponent_legal_moves :
        moyenne = moyenne + i
    if len(opponent_legal_moves) != 0 :
        moyenne = moyenne / len(opponent_legal_moves)
    if pos.turn == chess.WHITE :
        evaluation = evaluation + 0.1*(pos.legal_moves.count() - moyenne)
    else :
        evaluation = evaluation - 0.1*(pos.legal_moves.count() - moyenne)
    return evaluation

def evaluate(pos) :
    '''Évaluation d'une position.'''
    if pos.is_checkmate() :
        return -(-1+2*pos.turn) * infinity
    elif game_is_finished(pos) :
        return 0

    evaluation = 0
    evaluation = evaluation + materiel_eval(pos)
    if not pos.is_check() :
        evaluation = evaluation + mobility_eval(pos)
    evaluation = evaluation + 0.6*placement_eval(pos)
    evaluation = evaluation + attack_protect(pos)
    evaluation = evaluation + 0.1*king_safety(pos)
    return evaluation

def evaluation_turn(pos) :
    '''Évaluation d'une position selon le côté qui doit jouer.'''
    if pos.turn == chess.WHITE :
        return evaluate(pos)
    else :
        return - evaluate(pos)