import chess
from utils import VALUE_MATE, MAX_PLY, clamp
from typing import List
from see import VALUES, see_capture

MAX_HISTORY = 1000

# History heuristic store : hystory[PieceType][Square]
    # PieceType goes from 1 to 6
    # Square    goes from 0 to 63
history = [[0 for __ in chess.SQUARES] for _ in chess.PIECE_TYPES]
# Killer move store :
killers = [[chess.Move.null(), chess.Move.null()] for _ in range(MAX_PLY)]

def reset_tables() -> None :
    global history
    global killers
    
    history = [[0 for __ in chess.SQUARES] for _ in chess.PIECE_TYPES]
    killers = [[chess.Move.null(), chess.Move.null()] for _ in range(MAX_PLY)]

def update_history(piece: chess.PieceType, to: chess.Square, value: int) -> None :
    global history
    clampedBonus = clamp(value, MAX_HISTORY, -MAX_HISTORY)
    history[piece-1][to] += clampedBonus - history[piece-1][to] * abs(clampedBonus) / MAX_HISTORY

def update_killers(move: chess.Move, ply: int) -> None :
    global killers
    if killers[ply][0] == move :
        return
    if killers[ply][1] == move :
        killers[ply][0], killers[ply][1] = killers[ply][1], killers[ply][0]
        return
    killers[ply][1] = killers[ply][0]
    killers[ply][0] = move

# MVV_LVA[attacker][victim]
MVV_LVA = [
    # Victim      P    N    B    R    Q    K    / Attacker
                [105, 205, 305, 405, 505, 605], #    P
                [104, 204, 304, 404, 504, 604], #    N
                [103, 203, 303, 403, 503, 603], #    B
                [102, 202, 302, 402, 502, 602], #    R
                [101, 201, 301, 401, 501, 601], #    Q
                [100, 200, 300, 400, 500, 600], #    K
]

def score_move(move: chess.Move, board: chess.Board, ply: int, best_move: chess.Move=chess.Move.null()) -> int :
    ''' A method for move ordering. An heuristic to assign score to moves to
    search probable best moves at first, so that search is faster.'''

    score = 0

    if move == best_move :
        return VALUE_MATE
    
    if board.gives_check(move) :
        return 7000

    if board.is_en_passant(move) :
            return 105 # PxP
    if board.is_capture(move) : # If the move is a capture move
        # Apply MVV-LVA scoring. The idea is to say that taking a valuable piece
        # with a smaller piece (like PxQ) is probably better than taking a
        # smaller piece with a valuable one (like QxP).
        
        attacker_value = VALUES[board.piece_type_at(move.to_square)]
        victime_value  = VALUES[board.piece_type_at(move.from_square)]

        if attacker_value <= victime_value :
            return victime_value - attacker_value
        return see_capture(board, move)

        return MVV_LVA[board.piece_type_at(move.from_square)-1][board.piece_type_at(move.to_square)-1]

    # Else if the move is not a capture move, let's simply use Killer Moves and
    # History Heuristic
    if killers[ply][0] == move :
        score += 9000
    elif killers[ply][1] == move :
        score += 8000
    score +=  int(history[board.piece_type_at(move.from_square)-1][move.to_square])

    return score


def ordering(board: chess.Board, ply: int, moves: List[chess.Move], best_move: chess.Move=chess.Move.null()) -> List[chess.Move] :
    ''' A move ordering method. See score_move() '''
    Moves = [[move, score_move(move, board, ply, best_move)] for move in moves]
    Moves.sort(key=lambda a: a[1], reverse=True)
    return [m[0] for m in Moves]