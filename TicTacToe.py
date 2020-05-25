""" TicTacToe game """

from abc import ABC


class PlayField:
    """ Store game progress and game signs """
    status_draw = 0
    status_game = 9

    sign_o = -1
    empty = 0
    sign_x = +1

    encode_signs = {"O": sign_o, "_": empty, "X": sign_x}
    decode_signs = {sign_o: "O", empty: " ", sign_x: "X"}

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
        return self.status_game if self.empty in self.matrix else self.status_draw

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
    """ Store possible move methods """
    @staticmethod
    def manually(play_field: PlayField, sign: str) -> PlayField.get_field:
        while True:
            try:
                column, row = map(int, input("Enter the coordinates: ").split())
                if column not in range(1, 4) or row not in range(1, 4):
                    raise IndexError
                cell = 9 - row * 3 + column - 1
                if play_field.matrix[cell] != play_field.empty:
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


if __name__ == "__main__":
    PLAY_FIELD = PlayField()
    PLAY_FIELD.set_field(input("Enter cells: "))
    SIGN = "O" if sum(PLAY_FIELD.matrix) else "X"
    print(PLAY_FIELD.get_field())
    Move.manually(PLAY_FIELD, SIGN)
    print(PLAY_FIELD.__str__())
