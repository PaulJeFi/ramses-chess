import requests
import chess

def tablebase(board) :
    if len(board.piece_map()) <= 7 :
        try :
            fen = board.fen().replace(' ', '_')
            info = requests.get(f'http://tablebase.lichess.ovh/standard?fen={fen}')
            return info.json()['moves'][0]['uci']
        except Exception :
            pass
    return None