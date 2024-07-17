import math
import time
import chess
import chess.syzygy
import chess.polyglot
from chess.polyglot import zobrist_hash
from evaluation import evaluate
from tt import TT
from utils import VALUE_MATE, MAX_PLY, BOUND_LOWER, BOUND_UPPER, BOUND_EXACT
from utils import VALUE_TB, VALUE_TB_LOSS_IN_MAX_PLY, VALUE_TB_WIN_IN_MAX_PLY
from utils import mate_in, mated_in, clamp, send_message
from move_ordering import ordering, update_history, update_killers, reset_tables
from typing import List

USE_TB  = True
TB_PATH = './bases345'
TB_MIN_PIECES = 5

if USE_TB :
    tablebase = chess.syzygy.open_tablebase(TB_PATH)

BOOK_PATH = './8moves_v3.bin'

def get_book_move(board: chess.Board) -> chess.Move :
    book = chess.polyglot.MemoryMappedReader(BOOK_PATH)
    try :
        entry = book.weighted_choice(board)
    except IndexError :
        return chess.Move.null()
    return entry.move

tt = TT()

class Searcher :

    def __init__(self) :#, board: chess.Board, depth: int=5, time_: bool|int=False) -> None :
        pass
        #self.iterative_deepening(board, depth, time_)
    
    def pvSearch(self, alpha: int=-VALUE_MATE, beta: int=VALUE_MATE, depth: int=1) -> int :

        self.nodes += 1
        self.seldepth = max(self.seldepth, self.ply)

        # Timeout check-up
        if self.nodes % 1024 == 0 :
            if time.time()*1000 - self.start_time >= self.time_ :
                self.timeout = True
                return 0
        if self.timeout :
            return 0


        # Quiescence
        if depth <= 0 or self.ply >= MAX_PLY :
            score = self.quiesce(alpha, beta)
            tt.save(self.board, depth, BOUND_EXACT, score, self.ply, timeout=self.timeout)
            return score

        # Initialize node
        depth = min(depth, MAX_PLY-1)
        bound = BOUND_LOWER
        bestmove = chess.Move.null()
        in_check = self.board.is_check()

        # Draw by repetition or insufficient material
        if self.ply != 0 and (self.board.is_repetition(2) or self.board.is_insufficient_material()) and alpha < 0 :
            alpha = 0
            if alpha >= beta :
                return alpha

        # Mate distance pruning
        if self.ply > 0 :
            alpha = max(mated_in(self.ply), alpha)
            beta  = min(mate_in(self.ply + 1), beta)
            if alpha >= beta :
                return alpha

        # TT probe
        probe = tt.probe(self.board, depth, alpha, beta, self.ply)
        if probe != None :
            if probe[0] != None and self.ply != 0 and beta-alpha == 1 :
                return probe[0]
            bestmove = probe[1]

        # TB probe (logic taken from Stockfish)
        if self.ply > 0 and USE_TB and \
           chess.popcount(self.board.occupied) <= TB_MIN_PIECES :

            wdl = tablebase.get_wdl(self.board)

            if wdl != None :

                drawscore = 1
                tbValue = VALUE_TB - self.ply
                if wdl < -drawscore :
                    value = -tbValue
                elif wdl > drawscore :
                    value = tbValue
                else :
                    value = 2 * wdl * drawscore
                
                if wdl < -drawscore :
                    bound = BOUND_UPPER
                elif  wdl > drawscore :
                    bound = BOUND_LOWER
                else :
                    bound = BOUND_EXACT

                if bound == BOUND_EXACT or \
                  (bound == BOUND_LOWER and value >= beta) or \
                  (bound == BOUND_UPPER and value <= alpha) :
                    tt.save(self.board, depth, bound, value, self.ply, timeout=self.timeout)
                    return value

                if beta-alpha > 1 : # PV-node
                    if bound == BOUND_LOWER :
                        #bestValue = value,
                        alpha = max(alpha, value)
                    #else :
                    #    maxValue = value;

        evaluation = evaluate(self.board)

        # Futility pruning
        if probe != None and depth < 13 and evaluation - 120*depth >= beta \
           and evaluation >= beta and beta > VALUE_TB_LOSS_IN_MAX_PLY \
           and evaluation < VALUE_TB_WIN_IN_MAX_PLY :
            return beta + (evaluation - beta)//13
        
        # Null move pruning
        if beta-alpha == 1 and not in_check \
           and self.board.move_stack[-1] != chess.Move.null() \
           and evaluation >= beta and evaluation >= beta - 21 * depth + 390 \
           and chess.popcount(self.board.occupied_co[self.board.turn]) - chess.popcount(self.board.pawns & self.board.occupied_co[self.board.turn]) > 1 \
           and beta > VALUE_TB_LOSS_IN_MAX_PLY :
            
            R = min(int(evaluation- beta) / 202, 6) + depth / 3 + 5
            self.ply += 1
            self.board.push(chess.Move.null())
            value = -self.pvSearch(-beta, -beta+1, depth-R)
            self.board.pop()
            self.ply -= 1
        
            # verification search
            if value >= beta and value < VALUE_TB_WIN_IN_MAX_PLY :
                if depth < 16 :
                    return value
                v = self.pvSearch(beta-1, beta, depth-R)
                if v >= beta :
                    return value

        # Internal iterative reduction
        if probe != None and beta-alpha > 1 and depth > 5 :
            if probe[1] == None :
                depth -= 3
        if depth <= 0 :
            score = self.quiesce(alpha, beta)
            tt.save(self.board, depth, BOUND_EXACT, score, self.ply, timeout=self.timeout)
            return score
        

        # Move loop
        moves_tried = 0
        self.ply += 1
        for move in ordering(self.board, self.ply, self.board.legal_moves, bestmove) :

            # For MultiPV
            if MULTI_PV != 1 and self.ply == 1 and move in self.exclude :
                continue

            is_capture = self.board.is_capture(move)
            self.board.push(move)


            if moves_tried == 0 :
                score = -self.pvSearch(-beta, -alpha, depth-1)

            # Late move reduction : I'm not convinced
            elif depth >= 3 :
                if is_capture or move.promotion != None :
                    r = 3
                else :
                    r = 0.7844 + math.log(depth) * math.log(moves_tried) / 2.4696
                score = -self.pvSearch(-alpha-1, -alpha, depth-int(r)) # or continue ?
                if score > alpha and beta-alpha > 1 : # beta-alpha > 1 : PV node -> re-search
                    score = -self.pvSearch(-beta, -alpha, depth-1)
                
            else :
                score = -self.pvSearch(-alpha-1, -alpha, depth-1)
                if score > alpha and beta-alpha > 1 : # beta-alpha > 1 : PV node -> re-search
                    score = -self.pvSearch(-beta, -alpha, depth-1)

            self.board.pop()
            moves_tried += 1

            if score >= beta : # fail-hard beta-cutoff
                if not self.board.is_capture(move) :
                    update_history(self.board.piece_type_at(move.from_square), move.to_square, beta)
                    update_killers(move, self.ply)
                alpha = beta
                bound = BOUND_UPPER
                bestmove = move
                break
            if score > alpha :
                alpha = score
                bound = BOUND_EXACT
                bestmove = move

        self.ply -= 1

        # Stalemate and checkmate detection
        if moves_tried == 0 :
            bound = BOUND_EXACT
            if self.board.is_check() : # checkmate
                alpha = -VALUE_MATE
            else : # draw
                alpha = 0
        elif self.board.is_fifty_moves() :
            bound = BOUND_EXACT
            alpha = 0


        tt.save(self.board, depth, bound, alpha, self.ply, bestmove, timeout=self.timeout)
        return alpha # fail-hard
        
    def quiesce(self, alpha, beta) -> int :

        self.nodes += 1
        self.seldepth = max(self.seldepth, self.ply)

        # Timeout check-up
        if self.nodes % 1024 == 0 :
            if time.time()*1000 - self.start_time >= self.time_ :
                self.timeout = True
                return 0
        if self.timeout :
            return 0

        # Check for insufficient material
        if self.board.is_insufficient_material() and alpha < 0 :
            alpha = 0
            if alpha >= beta :
                return alpha
            
        # Mate distance pruning
        if self.ply > 0 :
            alpha = max(mated_in(self.ply), alpha)
            beta  = min(mate_in(self.ply + 1), beta)
            if alpha >= beta :
                return alpha
        
        stand_pat = evaluate(self.board)
        if stand_pat >= beta :
            return beta
        
        # Delta pruning
        delta = 975
        if chess.QUEEN in [move.promotion for move in self.board.legal_moves] :
            delta += 775
        if stand_pat < alpha - delta :
            return alpha

        if alpha < stand_pat :
            alpha = stand_pat

        # Mate distance pruning
        if self.ply > 0 :
            alpha = max(mated_in(self.ply), alpha)
            beta  = min(mate_in(self.ply + 1), beta)
            if alpha >= beta :
                return alpha
        
        self.ply += 1
        for move in ordering(self.board, self.ply, self.board.generate_legal_captures()) :

            self.board.push(move)
            score = -self.quiesce(-beta, -alpha)
            self.board.pop()

            if score >= beta :
                alpha = beta
                break
            if score > alpha :
                alpha = score
        
        self.ply -= 1

        # Stalemate and checkmate detection
        if self.board.is_checkmate() :
            alpha = -VALUE_MATE
        elif self.board.is_stalemate() :
            alpha = 0

        return alpha
    
    def PV(self) -> list[chess.Move] :
        
        stop = False
        PV = []

        while not stop :

            key = zobrist_hash(self.board)
            entry = tt.tt[key & (tt.size - 1)]

            if entry.key == key and entry.move != chess.Move.null() \
               and self.board.is_legal(entry.move) :

                PV.append(entry.move)
                self.board.push(entry.move)

                if self.board.is_repetition() :
                    stop = True
            
            else :
                stop = True

        for _ in PV :
            self.board.pop()
        
        return PV
    
    def iterative_deepening(self, board: chess.Board, depth: int=5, time_: bool|int=False) -> None :

        move = get_book_move(board)
        if move != chess.Move.null() and board.is_legal(move) :
            send_message('info depth 10 score cp 0 pv ' + str(move))
            send_message(f'bestmove {str(move)}')
            return
        
        moves = list(board.legal_moves)
        if not UCI_AnalyseMode :
            if len(moves) == 1 :
                time.sleep(1/10)
                send_message(f'info depth 1 score cp {evaluate(board)} pv {str(moves[0])}')
                send_message('bestmove ' + str(moves[0]))

        self.board = board
        self.nodes = 0
        self.ply = 0
        self.timeout = False
        self.seldepth = 0
        
        start_time = time.time() * 1000
        if time_ :
            depth = MAX_PLY
        else :
            time_ = float('inf')
        elapsed = time.time() * 1000 - start_time

        bestmove = ordering(board, 0, moves)[0]
        second_m = chess.Move.null()

        for curr_depth in range(1, depth+1) :

            exclude = []
            evaluation = VALUE_MATE

            for i in range(min(MULTI_PV, len(moves))) :

                self.depth = curr_depth
                self.time_ = time_-elapsed
                self.exclude = exclude
                self.start_time = time.time() * 1000
                self.nodes = 0
                self.ply = 0
                self.timeout = False
                self.seldepth = 0

                evaluation = self.pvSearch(depth=self.depth, beta=evaluation)
                elapsed = time.time() * 1000 - start_time

                if self.timeout :
                    send_message(f'bestmove {str(bestmove)} ponder {str(second_m)}')
                    return None

                PV = self.PV()
                exclude.append(PV[0])

                if i == 0 :
                    bestmove = PV[0]
                    if len(PV) > 1 :
                        second_m = PV[1]

                send_message(f'info depth {self.depth} seldepth {self.seldepth}', end=' ')
                send_message(multipv(i), end='')
                send_message(f'score {display_eval(evaluation)} nodes {self.nodes} nps', end=' ')
                send_message(f'{int(1000 * self.nodes / elapsed)} time {int(elapsed)} hashfull {tt.hashfull()} pv {' '.join([str(move) for move in PV])}')
            
            if elapsed >= time_ or curr_depth >= depth :
                send_message(f'bestmove {str(bestmove)} ponder {str(second_m)}')
                return None
    
MULTI_PV = 1
UCI_AnalyseMode = False

def multipv(i: int) -> str :
    if MULTI_PV == 1 :
        return ''
    return 'multipv ' + str(i+1) + ' '

def display_eval(evaluation: int) -> str :
    if evaluation >= VALUE_MATE - MAX_PLY or -evaluation >= VALUE_MATE - MAX_PLY :
        return 'mate ' + str((1 if evaluation > 0 else -1) * math.ceil((VALUE_MATE - math.ceil(abs(evaluation)))/2))
    return 'cp ' + str(evaluation) 

def manage(time_: int, board: chess.Board, inc: int, movestogo: int) -> int :
    if movestogo == 0 :
        Y = max(10, 40 - len(board.move_stack)/2)
        return math.floor(clamp(time_/Y + inc * Y/10, 0, time_))
    return math.floor(clamp(time_/movestogo + inc, 0, time_))