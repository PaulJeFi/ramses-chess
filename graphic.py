import pygame
import chess

size = 90

screen = pygame.display.set_mode((size*8, size*8))
pygame.display.set_caption("Chess Engine")
screen.fill("WHITE")

pygame.display.set_icon(pygame.image.load('/Users/pauljerome--filio/Documents/Python_files/Chess_engine/graph/icone.png').convert_alpha())

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = ((205+170)/2, (210+162)/2, (112+65)/2)

source = 'chesscom'
if source == 'chesscom' :
    ext = '.png'
elif source == 'lichess' :
    ext = '.svg'

chessboard = pygame.image.load('chess_set/150.png').convert_alpha()
King = pygame.image.load('chess_set/'+source+'/wk'+ext).convert_alpha()
king = pygame.image.load('chess_set/'+source+'/bk'+ext).convert_alpha()
Knight = pygame.image.load('chess_set/'+source+'/wn'+ext).convert_alpha()
knight = pygame.image.load('chess_set/'+source+'/bn'+ext).convert_alpha()
Rook = pygame.image.load('chess_set/'+source+'/wr'+ext).convert_alpha()
rook = pygame.image.load('chess_set/'+source+'/br'+ext).convert_alpha()
Queen = pygame.image.load('chess_set/'+source+'/wq'+ext).convert_alpha()
queen = pygame.image.load('chess_set/'+source+'/bq'+ext).convert_alpha()
Bishop = pygame.image.load('chess_set/'+source+'/wb'+ext).convert_alpha()
bishop = pygame.image.load('chess_set/'+source+'/bb'+ext).convert_alpha()
Pawn = pygame.image.load('chess_set/'+source+'/wp'+ext).convert_alpha()
pawn = pygame.image.load('chess_set/'+source+'/bp'+ext).convert_alpha()

chessboard = pygame.transform.scale(chessboard, (size*8, size*8))
King = pygame.transform.scale(King, (size, size))
king = pygame.transform.scale(king, (size, size))
Queen = pygame.transform.scale(Queen, (size, size))
queen = pygame.transform.scale(queen, (size, size))
Rook = pygame.transform.scale(Rook, (size, size))
rook = pygame.transform.scale(rook, (size, size))
Bishop = pygame.transform.scale(Bishop, (size, size))
bishop = pygame.transform.scale(bishop, (size, size))
Knight = pygame.transform.scale(Knight, (size, size))
knight = pygame.transform.scale(knight, (size, size))
Pawn = pygame.transform.scale(Pawn, (size, size))
pawn = pygame.transform.scale(pawn, (size, size))


def draw(fen, col, rank, board) :
    if fen == 'K' :
        if board.turn == chess.WHITE :
            if board.is_checkmate() :
                pygame.draw.rect(screen, RED, (rank, col, size, size))
            elif board.is_check() :
                pygame.draw.circle(screen, RED, (rank + size/2, col + size/2), size/2)
        screen.blit(King, (rank, col))
    elif fen == 'k' :
        if board.turn == chess.BLACK :
            if board.is_checkmate() :
                pygame.draw.rect(screen, RED, (rank, col, size, size))
            elif board.is_check() :
                pygame.draw.circle(screen, RED, (rank + size/2, col + size/2), size/2)
        screen.blit(king, (rank, col))
    elif fen == 'Q' :
        screen.blit(Queen, (rank, col))
    elif fen == 'q' :
        screen.blit(queen, (rank, col))
    elif fen == 'R' :
        screen.blit(Rook, (rank, col))
    elif fen == 'r' :
        screen.blit(rook, (rank, col))
    elif fen == 'N' :
        screen.blit(Knight, (rank, col))
    elif fen == 'n' :
        screen.blit(knight, (rank, col))
    elif fen == 'B' :
        screen.blit(Bishop, (rank, col))
    elif fen == 'b' :
        screen.blit(bishop, (rank, col))
    elif fen == 'P' :
        screen.blit(Pawn, (rank, col))
    elif fen == 'p' :
        screen.blit(pawn, (rank, col))

def place(move) :
    if move[0] == 'a' :
        col = 0
    elif move[0] == 'b' :
        col = 1
    elif move[0] == 'c' :
        col = 2
    elif move[0] == 'd' :
        col = 3
    elif move[0] == 'e' :
        col = 4
    elif move[0] == 'f' :
        col = 5
    elif move[0] == 'g' :
        col = 6 
    elif move[0] == 'h' :
        col = 7
    if move[1] == '8' :
        rank = 0
    elif move[1] == '7' :
        rank = 1
    elif move[1] == '6' :
        rank = 2
    elif move[1] == '5' :
        rank = 3
    elif move[1] == '4' :
        rank = 4
    elif move[1] == '3' :
        rank = 5
    elif move[1] == '2' :
        rank = 6 
    elif move[1] == '1' :
        rank = 7
    return (col*size, rank*size)

def show_move(move) :
    un = place(move)
    deux = place(move[2:4])
    pygame.draw.rect(screen, GREEN, (*un, size, size))
    pygame.draw.rect(screen, GREEN, (*deux, size, size))

def show(FEN, board, move) :
        screen.blit(chessboard, (0, 0))
        if move != None :
            show_move(move)
        col = 0
        rank = 0
        for fen in FEN :
            if fen == '/' :
                col = col + 1
                rank = 0
            elif fen in ('1', '2', '3', '4', '5', '6', '7', '8') :
                rank = rank + int(fen)
            elif fen in ('K', 'k', 'Q', 'q', 'R', 'r', 'N', 'n', 'B', 'b', 'P', 'p') :
                draw(fen, col*size, rank*size, board)
                rank = rank + 1
        pygame.display.update()
