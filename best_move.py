#import chess
import book
import search
from move_generation import get_ordered_moves

def best_move(board, timeleft=None, depth=2) :
    '''Détermine le meilleur coup.'''
    value = 0
    move = book.move_from_book(board, book.book)
    if move != None :
        #print("Book : {}".format(move))
        return move, 0
    else :
        #print("On commence à chercher le meilleur coup.")
        if type(timeleft) == int :
            time = timeleft/1000
            depth = 2
            if time > 18*60 :
                depth = 2
            elif time > 30 :
                depth = 2
            elif time > 3 :
                depth = 1
            elif time <= 5 :
                depth = 0
                #print("Mode survie activé.")
                #print("Aléatoire :", move)
        else :
            depth = depth
            #print("Erreur au niveau du temps, depth : {}".format(depth))
        if depth == 0 :
            move = get_ordered_moves(board)[0]
            value = 0
        else :
            move, value = search.search(board, depth)
        #print("On va faire", move)
        #print("Eval :", value)
        return str(move), value

def game_is_finished(pos) :
    '''Détermine si la partie est finie.'''
    if pos.is_checkmate() or pos.is_stalemate() or pos.is_insufficient_material() or pos.can_claim_threefold_repetition() :
        return True
    else :
        return False
