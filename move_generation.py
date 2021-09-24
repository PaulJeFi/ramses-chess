import chess
import eval

def move_value(board: chess.Board, move: chess.Move, endgame: bool) -> float :
    """
    How good is a move?
    A promotion is great.
    A weaker piece taking a stronger piece is good.
    A stronger piece taking a weaker piece is bad.
    Also consider the position change via piece-square table.
    """
    if move.promotion is not None :
        return -float("inf") if board.turn == chess.BLACK else float("inf")

    _piece = board.piece_at(move.from_square)
    if _piece :
        _from_value = evaluate_piece(_piece, move.from_square, endgame, board)
        _to_value = evaluate_piece(_piece, move.to_square, endgame, board)
        position_change = _to_value - _from_value
    else :
        raise Exception(f"A piece was expected at {move.from_square}")

    capture_value = 0.0
    if board.is_capture(move) :
        capture_value = evaluate_capture(board, move)

    current_move_value = capture_value + position_change
    if board.turn == chess.BLACK :
        current_move_value = -current_move_value

    return current_move_value


def evaluate_capture(board: chess.Board, move: chess.Move) -> float :
    """
    Given a capturing move, weight the trade being made.
    """
    piece_value = {
    chess.PAWN: 1,
    chess.ROOK: eval.rook_knight_value(board)[0],
    chess.KNIGHT: eval.rook_knight_value(board)[1],
    chess.BISHOP: 3,
    chess.QUEEN: 9,
    chess.KING:  eval.infinity}

    if board.is_en_passant(move) :
        return piece_value[chess.PAWN]
    _to = board.piece_at(move.to_square)
    _from = board.piece_at(move.from_square)
    if _to is None or _from is None :
        raise Exception(
            f"Pieces were expected at _both_ {move.to_square} and {move.from_square}"
        )
    return piece_value[_to.piece_type] - piece_value[_from.piece_type]


def evaluate_piece(piece: chess.Piece, square: chess.Square, end_game: bool, pos: chess.Board()) -> int :
    if eval.phase(pos) == 'Fin de partie' :
        # Référence aux listes selon les pièces.
        pieces = {'K': eval.K_end, 'k': eval.k_end, 'Q': eval.Q, 'q': eval.q, 'R': eval.R, 'r': eval.r, 'N': eval.N, 'n': eval.n, 'B': eval.B, 'b': eval.b, 'P': eval.P, 'p': eval.p}
    else :
        # Référence aux listes selon les pièces.
        
        pieces = {'K': eval.K, 'k': eval.k, 'Q': eval.Q, 'q': eval.q, 'R': eval.R, 'r': eval.r, 'N': eval.N, 'n': eval.n, 'B': eval.B, 'b': eval.b, 'P': eval.P, 'p': eval.p}

    piece_type = piece.symbol()
    mapping = pieces[piece_type]
    return mapping[square]

def get_ordered_moves(board: chess.Board) -> list[chess.Move]:
    """
    Get legal moves.
    Attempt to sort moves by best to worst.
    Use piece values (and positional gains/losses) to weight captures.
    """
    for move in board.legal_moves :
        board.push_san(str(move))
        if board.is_checkmate() :
            board.pop()
            return [move]
        else :
            board.pop()
    end_game = (eval.phase(board) == 'Fin de partie')

    def orderer(move):
        return move_value(board, move, end_game)

    in_order = sorted(
        board.legal_moves, key=orderer, reverse=(board.turn == chess.WHITE)
    )
    return list(in_order)