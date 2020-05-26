""" TicTacToe game """

from abc import ABC
from random import choice


class PlayField:
    """ Stores game progress and game signs """
    status_draw = 0
    status_game = 9

    sign_o = -1
    empty_cell = 0
    sign_x = +1

    encode_signs = {"O": sign_o, "_": empty_cell, "X": sign_x}
    decode_signs = {sign_o: "O", empty_cell: " ", sign_x: "X"}

    win_combinations = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
        (0, 4, 8), (2, 4, 6)              # diagonals
    )

    def __init__(self) -> None:
        self.matrix = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    def __repr__(self) -> int:
        """ Returns status of the game as integer """
        for combination in self.win_combinations:
            for sign in (self.sign_x, self.sign_o):
                cells_sum = sum(self.matrix[i] for i in combination)
                if cells_sum == sign * 3:
                    return cells_sum
        return self.status_game if self.empty_cell in self.matrix else self.status_draw

    def __str__(self) -> str:
        """ Returns status of the game as string """
        for sign in (self.sign_x, self.sign_o):
            if self.__repr__() == sign * 3:
                return f"{self.decode_signs[sign]} wins"
        return "Game not finished" if self.__repr__() == self.status_game else "Draw"

    def set_field(self, field: str) -> None:
        self.matrix = [self.encode_signs[sign] for sign in field]

    def get_field(self) -> str:
        _ = [self.decode_signs[sign] for sign in self.matrix]
        return f"""
---------
| {_[0]} {_[1]} {_[2]} |
| {_[3]} {_[4]} {_[5]} |
| {_[6]} {_[7]} {_[8]} |
---------
"""


class Move(ABC):
    """ Stores possible move methods """
    @staticmethod
    def manually(sign: str, play_field: PlayField) -> PlayField.get_field:
        while True:
            try:
                column, row = map(int, input("Enter the coordinates: ").split())
                if column not in range(1, 4) or row not in range(1, 4):
                    raise IndexError
                cell = 9 - row * 3 + column - 1
                if play_field.matrix[cell] != play_field.empty_cell:
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
            play_field.matrix[cell] = play_field.encode_signs[sign]
            return print(play_field.get_field())

    def randomly(self, sign: str, play_field: PlayField) -> PlayField.get_field:
        random_cell = choice(self._empties(play_field))
        play_field.matrix[random_cell] = play_field.encode_signs[sign]
        return print(play_field.get_field())

    @staticmethod
    def _empties(play_field: PlayField) -> list:
        cells = range(len(play_field.matrix))
        return [cell for cell in cells if play_field.matrix[cell] == play_field.empty_cell]


class Player:
    """ Stores player's state """
    possible_levels = ("user", "easy", "medium", "hard")

    def __init__(self, sign: str, level: str) -> None:
        self.sign = sign
        self.level = self._check(level)

    def _check(self, level: str) -> str:
        if level not in self.possible_levels:
            raise Exception("Unpossible Player")
        return level

    def making_move(self, play_field: PlayField) -> None:
        if self.level == "user":
            Move().manually(self.sign, play_field)

        if self.level == "easy":
            print(f'Making move level "{self.level}"')
            Move().randomly(self.sign, play_field)


if __name__ == "__main__":
    # Manual testing
    PLAY_FIELD = PlayField()
    PLAYER = {
        PLAY_FIELD.sign_x: Player("X", "user"),
        PLAY_FIELD.sign_o: Player("O", "easy")
    }
    TURN = PLAY_FIELD.sign_x
    print(PLAY_FIELD.get_field())
    while True:
        PLAYER[TURN].making_move(PLAY_FIELD)
        if PLAY_FIELD.__str__() != "Game not finished":
            break
        TURN = -TURN
    print(PLAY_FIELD.__str__())
