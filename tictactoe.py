""" TicTacToe game """

from abc import ABC
from random import choice

O_CELL = -1
EMPTY = 0
X_CELL = +1

GAME_DRAW = 0
NOT_FINISHED = 9
X_WINS = X_CELL * 3
O_WINS = O_CELL * 3

ENCODE = {"O": O_CELL, "_": EMPTY, "X": X_CELL}
DECODE = {O_CELL: "O", EMPTY: " ", X_CELL: "X"}

WIN_CELLS = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),  # rows
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),  # columns
    (0, 4, 8),
    (2, 4, 6),  # diagonals
)


class PlayField:
    """ Stores game progress"""

    def __init__(self):
        self.cells = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    def get_status_code(self) -> int:
        """ Returns status code of the current game progress """
        for combination in WIN_CELLS:
            cells_sum = sum(self.cells[i] for i in combination)
            if cells_sum == X_WINS:
                return X_WINS
            if cells_sum == O_WINS:
                return O_WINS
        return NOT_FINISHED if EMPTY in self.cells else GAME_DRAW

    def get_output(self) -> str:
        """ Returns play field as a string """
        _ = [DECODE[sign] for sign in self.cells]
        return f"""
---------
| {_[0]} {_[1]} {_[2]} |
| {_[3]} {_[4]} {_[5]} |
| {_[6]} {_[7]} {_[8]} |
---------
"""


class Player:
    """ Stores player's condition """

    possible_levels = ("user", "easy", "medium", "hard")

    def __init__(self, character: str, level: str):
        self.sign: int = ENCODE[character]
        self.level = self._check(level)

    def _check(self, level: str) -> str:
        if level not in self.possible_levels:
            raise ValueError("Impossible Player")
        return level

    def make_move(self, playfield: PlayField):
        if self.level == "user":
            ConcreteMove().user(self.sign, playfield)
        else:
            print(f'Making move level "{self.level}"')
            if self.level == "easy":
                ConcreteMove().easy(self.sign, playfield)
            if self.level == "medium":
                ConcreteMove().medium(self.sign, playfield)
            if self.level == "hard":
                ConcreteMove().hard(self.sign, playfield)
        print(playfield.get_output())


class ConcreteMove(ABC):
    """ Implements player's moves """

    @staticmethod
    def user(sign: int, playfield: PlayField):
        MoveStrategy().manually(sign, playfield)

    @staticmethod
    def easy(sign: int, playfield: PlayField):
        MoveStrategy().randomly(sign, playfield)

    @staticmethod
    def medium(sign: int, playfield: PlayField):
        """ Makes move if two similar signs in playfield combination will be found """

        def duplet(sign: int) -> list:
            """ Returns list with index of the empty cell """
            for combination in WIN_CELLS:
                if sum(playfield.cells[i] for i in combination) == sign * 2:
                    return [i for i in combination if playfield.cells[i] == EMPTY]

        for case in (sign, -sign):
            index = duplet(case)
            if index:
                playfield.cells[index[0]] = sign
                break
        else:
            MoveStrategy().randomly(sign, playfield)

    @staticmethod
    def hard(sign: int, playfield: PlayField):
        depth = len(MoveStrategy().empty_cells(playfield))
        if depth < 9:
            index, _ = MoveStrategy().minimax(sign, playfield, depth)
            playfield.cells[index] = sign
        else:
            MoveStrategy().randomly(sign, playfield)


class MoveStrategy(ABC):
    """ Implements possible move strategies """

    def randomly(self, sign: int, playfield: PlayField):
        """ Random move """
        random_index = choice(self.empty_cells(playfield))
        playfield.cells[random_index] = sign

    def minimax(self, sign: int, playfield: PlayField, depth: int) -> list:
        """
        The adapted version of the minimax algorithm from:
        https://github.com/Cledersonbc/tic-tac-toe-minimax
        """
        maximizing = sign == X_CELL
        best_case = [EMPTY, O_WINS if maximizing else X_WINS]

        if playfield.get_status_code() != NOT_FINISHED:
            best_case[-1] = playfield.get_status_code()
            return best_case

        for i in self.empty_cells(playfield):
            playfield.cells[i] = sign
            current_case = self.minimax(-sign, playfield, depth - 1)
            current_case[0] = i
            playfield.cells[i] = EMPTY

            def get(comparator: max or min):
                return comparator(current_case, best_case, key=lambda i: i[-1])

            best_case = get(max) if maximizing else get(min)
        return best_case

    @staticmethod
    def manually(sign: int, playfield: PlayField):
        """ Handlings manual user input and check them """
        while True:
            try:
                column, row = map(int, input("Enter the coordinates: ").split())
                if column not in range(1, 4) or row not in range(1, 4):
                    raise IndexError
                index = 9 - row * 3 + column - 1
                if playfield.cells[index] != EMPTY:
                    raise AssertionError
            except ValueError:
                print("You should enter numbers!")
                continue
            except IndexError:
                print("Coordinates should be from 1 to 3!")
                continue
            except AssertionError:
                print("This cell is occupied! Choose another one!")
                continue
            playfield.cells[index] = sign
            break

    @staticmethod
    def empty_cells(playfield: PlayField) -> list:
        """ Returns indexes of an empty cells """
        indexes = range(NOT_FINISHED)
        return [i for i in indexes if playfield.cells[i] == EMPTY]


def main():
    """ Handling game process """
    while True:
        arguments = input("Enter the commands: ").split()
        if (len(arguments) == 1) & (arguments[0] == "exit"):
            break
        try:
            if (len(arguments) == 3) | (arguments[0] == "start"):
                Player("X", arguments[1])
                Player("O", arguments[2])
            else:
                raise ValueError
        except ValueError:
            print("Bad parameters!")
            continue
        player = {X_CELL: Player("X", arguments[1]), O_CELL: Player("O", arguments[2])}
        playfield = PlayField()
        print(playfield.get_output())
        turn = X_CELL
        while True:
            player[turn].make_move(playfield)
            if playfield.get_status_code() != NOT_FINISHED:
                break
            turn = -turn
        character = DECODE[turn]
        print("Draw" if not playfield.get_status_code() else f"{character} wins")


if __name__ == "__main__":
    main()
