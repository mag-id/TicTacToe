# TicTacToe

Study project from [JetBrains Academy](https://hyperskill.org/projects?goal=7) which is a part of the [Python Developer](https://hyperskill.org/knowledge-map) track. Stages 1 - 5 were checked by JetBrains Academy system.

## Usage

### Run

    python tictactoe.py

### Enter the commands

    TicTacToe game, enter help for more information
    Enter the commands: 

### help

    TicTacToe game.
    ---------------

        Commands:
        'help'                  - print TicTacToe help information.
        'exit'                  - exit TicTecToe.
        'start' 'level' 'level' - start the game of the 'X' against 'O'.

        Possible 'X's and 'O's levelling:
        'hard'   - Chooses the best strategy the from start.
        'medium' - Chooses cell in combination if finds two similar signs in it.
        'easy'   - Chooses cell randomly.
        'user'   - User manual input.

        User input format: 'column number' 'row number'.
              ---------
        r:  3 | O X X |
        o:  3 | X O X |
        w:  1 | X X O |
              ---------
        column: 1 2 3

### Example

    Enter the commands: start hard user

    ---------
    |       |
    |       |
    |       |
    ---------

    Making move level "hard"

    ---------
    |       |
    |   X   |
    |       |
    ---------

    Enter the coordinates: 1 1

    ---------
    |       |
    |   X   |
    | O     |
    ---------

    Making move level "hard"

    ---------
    |       |
    |   X   |
    | O   X |
    ---------

    Enter the coordinates: 

## Implementation plan:
- [X] [Stage 1](https://hyperskill.org/projects/82/stages/452/implement) - Play field and its output.
- [X] [Stage 2](https://hyperskill.org/projects/82/stages/453/implement) - An easy level of difficulty level and user input.
- [X] [Stage 3](https://hyperskill.org/projects/82/stages/454/implement) - Menu commands (exit, start, easy, user).
- [X] [Stage 4](https://hyperskill.org/projects/82/stages/455/implement) - A medium level of difficulty.
- [X] [Stage 5](https://hyperskill.org/projects/82/stages/456/implement) - A hard level of difficulty (MiniMax algorithm).
- [X] [tictactoe.py](tictactoe.py) - Refactoring.

You can read more information about the project [here](https://hyperskill.org/projects/82?goal=391).
