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
        self.field = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    def __repr__(self) -> int:
        """ Returns status of the game as integer """
        for combination in self.win_combinations:
            for sign in (self.sign_x, self.sign_o):
                cells_sum = sum(self.field[i] for i in combination)
                if cells_sum == sign * 3:
                    return cells_sum
        return self.status_game if self.empty_cell in self.field else self.status_draw

    def __str__(self) -> str:
        """ Returns status of the game as string """
        for sign in (self.sign_x, self.sign_o):
            if self.__repr__() == sign * 3:
                return f"{self.decode_signs[sign]} wins"
        return "Game not finished" if self.__repr__() == self.status_game else "Draw"

    def set_field(self, field: str) -> None:
        self.field = [self.encode_signs[sign] for sign in field]

    def get_field(self) -> str:
        _ = [self.decode_signs[sign] for sign in self.field]
        return f"""
---------
| {_[0]} {_[1]} {_[2]} |
| {_[3]} {_[4]} {_[5]} |
| {_[6]} {_[7]} {_[8]} |
---------
"""


class Player:
    """ Stores player's state """
    possible_levels = ("user", "easy", "medium", "hard")

    def __init__(self, sign: str, level: str) -> None:
        self.sign = sign
        self.level = self._check(level)

    def _check(self, level: str) -> str:
        if level not in self.possible_levels:
            raise ValueError("Unpossible Player")
        return level

    def make_move(self, play_field: PlayField) -> None:
        if self.level == "user":
            ConcreteMove().user(self.sign, play_field)
        else:
            print(f'Making move level "{self.level}"')
            if self.level == "easy":
                ConcreteMove().easy(self.sign, play_field)
            if self.level == "medium":
                ConcreteMove().medium(self.sign, play_field)
            if self.level == "hard":
                ConcreteMove().hard(self.sign, play_field)
        print(play_field.get_field())


class ConcreteMove(ABC):
    """ Implements concrete player's moves """
    @staticmethod
    def user(sign: str, play_field: PlayField) -> None:
        MoveStrategy().manually(sign, play_field)

    @staticmethod
    def easy(sign: str, play_field: PlayField) -> None:
        MoveStrategy().randomly(sign, play_field)

    @staticmethod
    def medium(sign: str, play_field: PlayField) -> None:
        sign = play_field.encode_signs[sign]
        for case in (sign * 2, -sign * 2):
            for combination in play_field.win_combinations:
                cells = sum(play_field.field[i] for i in combination)
                if cells == case:
                    for i in combination:
                        if play_field.field[i] == play_field.empty_cell:
                            play_field.field[i] = sign
                            return
        sign = play_field.decode_signs[sign]
        MoveStrategy().randomly(sign, play_field)

    @staticmethod
    def hard(sign: str, play_field: PlayField) -> None:
        pass


class MoveStrategy(ABC):
    """ Implements possible move strategies """
    def randomly(self, sign: str, play_field: PlayField) -> None:
        random_cell = choice(self._empties(play_field))
        play_field.field[random_cell] = play_field.encode_signs[sign]

    def minimax(self):
        pass

    @staticmethod
    def manually(sign: str, play_field: PlayField) -> None:
        while True:
            try:
                column, row = map(int, input("Enter the coordinates: ").split())
                if column not in range(1, 4) or row not in range(1, 4):
                    raise IndexError
                cell = 9 - row * 3 + column - 1
                if play_field.field[cell] != play_field.empty_cell:
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
            play_field.field[cell] = play_field.encode_signs[sign]
            break

    @staticmethod
    def _empties(play_field: PlayField) -> list:
        cells = range(len(play_field.field))
        return [cell for cell in cells if play_field.field[cell] == play_field.empty_cell]


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

        play_field = PlayField()
        player = {
            play_field.sign_x: Player("X", arguments[1]),
            play_field.sign_o: Player("O", arguments[2])
        }
        turn = play_field.sign_x
        print(play_field.get_field())
        while True:
            player[turn].make_move(play_field)
            if play_field.__str__() != "Game not finished":
                break
            turn = -turn
        print(play_field.__str__())


if __name__ == "__main__":
    main()
