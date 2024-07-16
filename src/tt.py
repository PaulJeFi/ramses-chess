import chess
from chess.polyglot import zobrist_hash
from sys import getsizeof
import math
from typing import Tuple
from utils import VALUE_MATE, MAX_PLY, BOUND_LOWER, BOUND_UPPER, BOUND_EXACT



class Entry :
    '''A class that represents a TT entry'''
    
    key:   int = 0
    depth: int = -1
    value: int = 0
    flag:  int = -1
    move:  chess.Move = chess.Move.null()

    def __str__(self) -> str :
        return f'Key {hex(self.key)}\nDepth {self.depth}\nValue {self.value}\n'\
             + f'Flag {self.flag}\nMove {str(self.move)}'

class TT :

    def __init__(self, mbsize: int=256) -> None :
        self.resize(mbsize)

    def resize(self, mbsize: int) -> None :
        self.size = 2**math.floor(20 + math.log2(mbsize / getsizeof(Entry())))
        # size is now a power of 2, it is faster to access index : usually
        # computed with formula index = hash % size,
        # now we have the new : index = hash & (size - 1)
        # https://graphics.stanford.edu/~seander/bithacks.html#ModulusDivisionEasy
        # This is a comon hack in chessprogramming TT 
        self.tt = [Entry() for _ in range(self.size)]
    
    def clear(self) -> None :
        self.tt = [Entry() for _ in range(self.size)]

    def score_to_tt(self, score: int, ply: int) -> int :
        if score >= VALUE_MATE - 2 * MAX_PLY :
              return score + ply
        elif score <= -(VALUE_MATE - 2 * MAX_PLY) :
             return score - ply
        return score
    
    def score_from_tt(self, score: int, ply: int, rule50: int) -> int :

        if score >= VALUE_MATE - 2 * MAX_PLY : # win
            if score >= VALUE_MATE - MAX_PLY and VALUE_MATE - score > 99 - rule50 :
                return VALUE_MATE - MAX_PLY - 1 # return only true mate score
            return score - ply


        if score <= -(VALUE_MATE - 2 * MAX_PLY) : # loss
            if score <= -(VALUE_MATE - MAX_PLY) and VALUE_MATE + score > 99 - rule50 :
                return -(VALUE_MATE - MAX_PLY) + 1 # return only true mate score
            return score + ply
        return score

    def probe(self, board: chess.Board, depth: int, alpha: int, beta: int, ply: int) -> Tuple[int, chess.Move] | Tuple[None, chess.Move] | None:

        hash_ = zobrist_hash(board)
        entry = self.tt[hash_ & (self.size-1)]

        if hash_ == entry.key :

            if depth <= entry.depth :
                value = self.score_from_tt(entry.value, ply, board.halfmove_clock)
                if entry.flag == BOUND_EXACT :
                    return (value, entry.move)
                if entry.flag == BOUND_LOWER and value <= alpha :
                    return (alpha, entry.move)
                if entry.flag == BOUND_UPPER and value >= beta :
                    return (beta, entry.move)
                
            return (None, entry.move)

        return None
    
    def save(self, board: chess.Board, depth: int, flag: int, value: int, ply: int, move: chess.Move=chess.Move.null(), timeout: bool=False) -> None :

        if timeout :
            return None

        hash_ = zobrist_hash(board)
        entry = self.tt[hash_ & (self.size-1)]

        if hash_ == entry.key and entry.depth > depth :
            return None
        if hash_ != entry.key or move != chess.Move.null() : # we can keep the old ttmove if we have the same hash but no new move
            entry.move  = move

        entry.key   = hash_
        entry.depth = depth
        entry.value = self.score_to_tt(value, ply)
        entry.flag  = flag
        self.tt[hash_ & (self.size-1)] = entry

    def hashfull(self) -> int :

        counter = 0
        for i in range(min(self.size, 1000)) :
            if self.tt[i].flag != -1 :
                counter += 1
        if self.size >= 1000 :
            return counter
        return math.ceil(1000 * counter / self.size)