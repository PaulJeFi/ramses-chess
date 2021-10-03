import chess
import random
import json

book = 'book.json'

def move_from_book(the_board, Book) :
    '''Renvoie un mouvement du répertoire si la position y est.'''
    with open(Book, "r") as Table :
        table = json.load(Table)
    try :
        return random.choice(table[the_board.fen()])
    except Exception :
        return None
