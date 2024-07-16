# Ramsès-Chess

Réglisse is a chess engine using [```python-chess```](https://python-chess.readthedocs.io/en/latest/).


It currently has the following features :

- [Book](https://www.chessprogramming.org/Opening_Book) : [Polyglott book](http://hgm.nubati.net/book_format.html) support
- [Evaluation](https://www.chessprogramming.org/Evaluation)
    - [PSQT](https://www.chessprogramming.org/Piece-Square_Tables) eval
    - [material balance](https://www.chessprogramming.org/Material)
    - [tapered eval](https://www.chessprogramming.org/Tapered_Eval)
    - [Mop-up evaluation](https://www.chessprogramming.org/Mop-up_Evaluation)
    - [Trapped bisops](https://www.chessprogramming.org/Trapped_Pieces)
    - [Minor pieces development](https://www.chessprogramming.org/Development)
    - [Center control](https://www.chessprogramming.org/Center_Control) : [Pawn center](https://www.chessprogramming.org/Pawn_Center)
    - [Unadvanced central pawns](https://www.chessprogramming.org/Development#Eval_Considerations)
    - [space control eval](https://www.chessprogramming.org/Space)
    - [Doubled pawns](https://www.chessprogramming.org/Doubled_Pawn)
    - [Isolated pawns](https://www.chessprogramming.org/Isolated_Pawn)
    - [Rook on semi-open files](https://www.chessprogramming.org/Half-open_File)
    - [Rook on open-files](https://www.chessprogramming.org/Rook_on_Open_File)
    - [King safety](https://www.chessprogramming.org/King_Safety)
- [Search](https://www.chessprogramming.org/Search)
    - [EGTB](https://www.chessprogramming.org/Endgame_Tablebases) : [Syzygy](https://www.chessprogramming.org/Syzygy_Bases)
    - [PVS](https://www.chessprogramming.org/Principal_Variation_Search)
    - [PV](https://www.chessprogramming.org/Principal_Variation) store : From TT
    - [TT](https://www.chessprogramming.org/Transposition_Table)
        - [Zobrist Hashing](https://www.chessprogramming.org/Zobrist_Hashing) (in ```python-chess```)
    - [Null Move Pruning](https://www.chessprogramming.org/Null_Move_Pruning)
    - [LMR](https://www.chessprogramming.org/Late_Move_Reductions)
    - [Futility Pruning](https://www.chessprogramming.org/Futility_Pruning)
    - [iterative deepening](https://www.chessprogramming.org/Iterative_Deepening)
    - [mate distance pruning](https://www.chessprogramming.org/Mate_Distance_Pruning)
    - [Quiescence Search](https://www.chessprogramming.org/Quiescence_Search)
        - [delta pruning](https://www.chessprogramming.org/Delta_Pruning)
    - [Move Orderning](https://www.chessprogramming.org/Move_Ordering)
        - [MVV LVA](https://www.chessprogramming.org/MVV-LVA)
        - [History Heuristic](https://www.chessprogramming.org/History_Heuristic)
        - [Killer Moves Heuristic](https://www.chessprogramming.org/Killer_Heuristic)
        - [TT score](https://www.chessprogramming.org/Transposition_Table)
- [UCI](./engine-interface.md) interface (almost fully supported)

## Why _Ramsès_ ?
I took a cat name. Ramsès is one of my friend's cat.

## LICENSE
See the [license file](./LICENSE.txt) to know more about legal stuffs.

## How to use
You can run Réglisse in your favorite UCI GUI or in the terminal with [this script](./src/exe.sh). You may have to authorize access to this script first (```$ chmod +x [path to scipt]``` on MacOS and Linux). You need [node](https://nodejs.org/en/) to run Réglisse locally. You may have to modify ```/usr/local/bin/python3``` on [the script](./src/exe.sh) to the path to node on your system.