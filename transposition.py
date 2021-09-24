from typing import Any
import chess
import json

'''
Ajout des tables de transpositions. Les tables de transpositions sont
utilisées pour réduire le temps de calcul de l'algorithme de recherches.
Elles regroupent toutes les positions évaluées avec leur profondeur de
recherche et leur évaluation pour pouvoir s'en resservire plus tard, plutôt
que de passer du temps sur des positions évaluées.

Les données sont stucturées au format suivant :

{str(chess.Board()._transposition_key()(type: dict)): {"depth": int, "eval": float}}
'''

def find_eval(board: chess.Board(), depth: int) -> (float or Any) :
    '''Retourne l'évaluation de la position si elle est dans
    la table de transposition avec une depth supérieure ou égale.'''

    try :
        with open("transposition.json", "r") as Table :
            try :
                table = json.load(Table)
            except Exception :
                table = None
    except FileNotFoundError :
        # Si le fichier des tables de transpositions n'existe pas, on le crée.
        with open("transposition.json", "w") :
            pass
        return None
    if table == None :
        return None
    for transposition in table :
        if transposition == str(board._transposition_key()) :
            if table[transposition]["depth"] >= depth :
                return table[transposition]["eval"]

def add_eval(board: chess.Board(), depth: int, eval: float) -> None:
    '''Ajoute l'évaluation à la table de transposition.
    Écrase toutes les autres depth de cette position
    (notre depth actuelle est supposée être supérieure
    aux autres depth de cette position.'''

    with open("transposition.json", "r") as Table :
        try :
            table = json.load(Table)
        except Exception :
            table = {}
    if abs(eval) == float('inf') :
        return # Pas besoin d'ajouter une position d'échec et mat aux tables.
    table[str(board._transposition_key())] = {"depth": depth, "eval": eval}
    with open("transposition.json", "w") as Table :
        json.dump(table, Table)