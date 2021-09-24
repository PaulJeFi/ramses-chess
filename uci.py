from best_move import best_move as engine
import chess

def search(board, time=None, depth=2) :
    move, value = engine(board, depth=depth)
    print('bestmove {move}'.format(move=move))
    return str(move)

def get_fen(board) :
    print(board.fen())

def separate_moves(string) :
    string+= ' '
    liste = []
    word = ''
    for char in string :
        if char == ' ' :
            liste.append(word)
            word = ''
        elif string[-1] == char :
            liste.append(word)
            word = ''
        else :
            word += char
    moves = []
    for pot_move in liste :
        if (len(pot_move) == 4 or len(pot_move) == 5) and pot_move != 'moves' :
            moves.append(pot_move)
    return moves

def extract_fen(command) :
        old_space = 0
        old_char = ''
        number = '1234567890'
        string = ''
        for char in command :
            if char != ' ' :
                string += char
                old_char = char
                old_space = 0
            elif char == ' ' :
                if old_space == 0 :
                    string += char
                    old_char = char
                    old_space = 1
                elif old_char in number :
                    return string
        return string


board = chess.Board()
depth = 2
while True :
    command = input()

    if 'uci' in command :
        print('id name Ramsès-Chess\nid author Paul JÉRÔME--FILIO\noption name Depth type spin default 2 min 0 max 3\nuciok')
    
    elif 'isready' in command :
        print('readyok')

    elif 'debug' in command :
        pass
    
    elif command[0:8] == 'position' :
        ok = 0
        if command[9:12] == 'fen' :
            fen = extract_fen(command[13:])
            board = chess.Board(fen)
            ok += 1
        if 'startpos' in command :
            board = chess.Board()
            ok += 1
        if 'moves' in command :
            command += ' '
            ok += 1
            moves = separate_moves(command)
            for move in moves :
                if board.is_legal(chess.Move.from_uci(move)) :
                    board.push_uci(move)
        if ok == 0 :
            help()

    elif 'go' in command :
        if 'depth' in command :
            search(board, depth=int(command[9]))
        else :
            search(board, depth=depth)

    elif command == 'stop' :
        pass

    elif 'setoption' in command :
        if 'Depth' in command :
            depth = int(command[16])
    
    #elif command == 'get FEN' :
    #    get_fen(board)

    #elif command == 'display' :
    #    print(board)

    #elif command == 'makebest' :
    #    board.push(chess.Move.from_uci(search(board)))

    elif command == 'ucinewgame' :
        board = chess.Board()

    #elif command == 'help' :
    #    help()
    
    elif command == 'quit' :
        quit()

    else :
        if command == '0000' :
            pass
        try :
            board.push_uci(command)
            #else :
            #    print('Illegal move :', command)
        except Exception :
            #print('Unknow command :', command)
            #help()
            pass