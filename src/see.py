import chess

VALUES = {chess.PAWN   : 100,
          chess.KNIGHT : 300,
          chess.BISHOP : 320,
          chess.ROOK   : 500,
          chess.QUEEN  : 900,
          chess.KING   : 10000}

def get_smallest_attacker(board: chess.Board, square: chess.Square) -> chess.Move | None :
    moves = list(board.generate_legal_captures(to_mask=chess.BB_SQUARES[square]))
    if len(moves) == 0 :
        return None
    return min(moves, key=lambda move: VALUES[board.piece_type_at(move.from_square)])

def see(board: chess.Board, square: chess.Square) -> int :
    value = 0
    move = get_smallest_attacker(board, square)
    if move != None :
        just_captured = VALUES[board.piece_type_at(square)]
        board.push(move)
        value = max(0, just_captured - see(board, square))
        board.pop()
    return value

def see_capture(board: chess.Board, move: chess.Move) -> int :
    value = 0
    just_captured = VALUES[board.piece_type_at(move.to_square)]
    board.push(move)
    value = just_captured - see(board, move.to_square)
    board.pop()
    return value

#print(see_capture(chess.Board('1k1r3q/1ppn3p/p4b2/4p3/8/P2N2P1/1PP1R1BP/2K1Q3 w - -'), chess.Move.from_uci('d3e5')))