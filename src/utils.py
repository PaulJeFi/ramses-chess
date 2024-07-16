from sys import stdout

DEBUG = False

BOUND_EXACT = 0
BOUND_LOWER = 1 # alpha
BOUND_UPPER  = 2 # beta

VALUE_MATE = 32000
MAX_PLY = 256

VALUE_MATE_IN_MAX_PLY  = VALUE_MATE - MAX_PLY
VALUE_MATED_IN_MAX_PLY = -VALUE_MATE_IN_MAX_PLY

VALUE_TB                 = VALUE_MATE_IN_MAX_PLY - 1
VALUE_TB_WIN_IN_MAX_PLY  = VALUE_TB - MAX_PLY
VALUE_TB_LOSS_IN_MAX_PLY = -VALUE_TB_WIN_IN_MAX_PLY

def clamp(x: float, mini: float, maxi: float) -> float :
    return max(mini, min(x, maxi))

def mate_in(ply: int) -> int :
    return VALUE_MATE - ply

def mated_in(ply: int) -> int :
    return -VALUE_MATE + ply

def send_message(text: str='', end: str='\n') -> None :

    stdout.write(text + end)
    stdout.flush()

    if DEBUG :
            with open('./log.txt', 'a') as file :
                file.write(text+end)