import chess
import search
from utils import clamp, DEBUG, send_message
import threading
import sys

def pretty_fen(fen) :
    FEN = ''
    for i in ''.join(fen.replace('/', '').split(' ')[0]) :
        if i.isdigit() :
            FEN += int(i) * ' '
        else :
            FEN += i

    board = ' +---+---+---+---+---+---+---+---+'
    count = 0
    for i in range(8) :
        board += '\n'
        for j in range(8) :
            board += ' | ' + FEN[count]
            count += 1
        board += ' | ' + str(8-i)
        board += '\n +---+---+---+---+---+---+---+---+'
    board += '\n   a   b   c   d   e   f   g   h'
    board += '\n\nFen : ' + fen

    return board

if __name__ == '__main__' :

    board = chess.Board()
    UseBook = True
    searcher = search.Searcher()
    thread = None

    send_message('KoshKa by Paul JF')

    while True :

        inp = input().split()
        
        if DEBUG :
            with open('./log.txt', 'a') as file :
                file.write(' '.join(inp)+'\n')

        try :
            
            if inp[0] == 'uci' :
                send_message('id name KoshKa\nid author Paul JF\n')
                send_message('option name Hash type spin default 256 min 1 max 33554432')
                send_message('option name Clear Tables type button')
                send_message('option name Skill type spin default 20 min 0 max 20')
                send_message('option name Book type string default <empty>')
                send_message('option name SyzygyPath type string default <empty>')
                send_message('option name MultiPV type spin default 1 min 1 max 500')
                send_message('uciok')

            elif inp[0] == 'isready' :
                send_message('readyok')

            elif inp[0] == 'ucinewgame' :
                board = chess.Board()
                search.reset_tables()
                search.tt.clear()

            elif inp[0] == 'd' :
                send_message()
                send_message(pretty_fen(board.fen()))
                send_message('Key : {}'.format(
                    hex(search.zobrist_hash(board))[2:].upper()))
            
            elif inp[0] == 'eval' :
                view = 1 if board.turn else -1
                send_message('Static eval : {} cp'.format(
                    search.evaluation.evaluate(board) * view
                ))

            elif inp[0] == 'quit' :
                sys.exit()

            elif inp[0] == 'position' :

                try : # if fen is invalid

                    if inp[1] == 'startpos' :
                        board = chess.Board()

                    elif inp[1] == 'fen' :

                        if 'moves' in inp :
                            board = chess.Board(
                                ' '.join(inp[2:inp.index('moves')])
                                )
                        else :
                            board = chess.Board(' '.join(inp[2:]))

                    if 'moves' in inp :
                        for move in inp[inp.index('moves')+1:] :
                            try :
                                move = chess.Move.from_uci(move.lower())
                                if board.is_legal(move) :
                                    board.push(move)
                            except chess.InvalidMoveError :
                                send_message('info string invalid moves')
                            

                except Exception :
                    send_message('info string invalid FEN')

            elif inp[0] == 'go' :

                depth = 3
                time_ = False
                inc = 0
                movestogo = 0

                if 'depth' in inp :
                    depth = int(inp[inp.index('depth')+1])
                
                if 'movestogo' in inp :
                    movestogo = int(inp[inp.index('movestogo')+1])

                if 'movetime' in inp :
                    time_ = int(inp[inp.index('movetime')+1])
                
                elif board.turn == chess.WHITE :
                    winc = 0
                    wtime = 0
                    if 'wtime' in inp :
                        wtime = int(inp[inp.index('wtime')+1])
                    if 'winc' in inp :
                        winc = int(inp[inp.index('winc')+1])
                    time_ = search.manage(wtime, board, winc, movestogo)
                
                elif board.turn == chess.BLACK :
                    binc = 0
                    btime = 0
                    if 'btime' in inp :
                        btime = int(inp[inp.index('btime')+1])
                    if 'binc' in inp :
                        binc = int(inp[inp.index('binc')+1])
                    time_ = search.manage(btime, board, binc, movestogo)

                #t = threading.Thread(target=search.Searcher, daemon=False, args=[board, depth, time_])
                #t.start()
                thread = threading.Thread(target=searcher.iterative_deepening, args=[board, depth, time_])
                thread.start()
            
            elif inp[0] == 'stop' :
                searcher.timeout = True
                try :
                    thread.join()
                except :
                    pass

            elif inp[0] == 'setoption' and inp[1] == 'name':

                if 'Clear' in inp and 'Tables' in inp :
                    search.reset_tables()
                    search.tt.clear()

                if 'UseBook' in inp and 'value' in inp :
                    search.BOOK_PATH = inp[-1]

                if 'MultiPV' in inp :
                    search.MULTI_PV = clamp(int(inp[-1]), 1, 500)

                if 'SyzygyPath' in inp :
                    search.TB_PATH = inp[-1]
                
                if 'Hash' in inp :
                    search.tt.resize(int(inp[-1]))
                
                if 'Skill' in inp :
                    search.evaluation.SKILL = clamp(int(inp[-1]), 0, 20)

        except IndexError :
            pass