""" tests by PyTest """

import tictactoe

FIELD = tictactoe.PlayField()
STRATEGY = tictactoe.MoveStrategy()
CONCRETE = tictactoe.ConcreteMove()


class TestPlayField:

    @staticmethod
    def test__repr__():
        cases = {
            # set_field input: __repr__ output
            "XXXOO_OX_": tictactoe.PlayField.sign_x * 3,
            "XX_XOXOOO": tictactoe.PlayField.sign_o * 3,
            "OXXXOOOXX": tictactoe.PlayField.status_draw,
            "_XO_OXX__": tictactoe.PlayField.status_game
        }
        for case, reference in cases.items():
            FIELD.set_field(case)
            assert FIELD.__repr__() == reference

    @staticmethod
    def test__str__():
        cases = {
            # set_field input: __str__ output
            "XXXOO_OX_": "X wins",
            "XX_XOXOOO": "O wins",
            "OXXXOOOXX": "Draw",
            "_XO_OXX__": "Game not finished"
        }
        for case, reference in cases.items():
            FIELD.set_field(case)
            assert FIELD.__str__() == reference

    @staticmethod
    def test_set_field():
        cases = {
            # set_field input: field state
            "_XXOO_OX_": [0, 1, 1, -1, -1, 0, -1, 1, 0],
            "XX_XOXOO_": [1, 1, 0, 1, -1, 1, -1, -1, 0],
            "OX_XOOOXX": [-1, 1, 0, 1, -1, -1, -1, 1, 1],
            "_XO_OX___": [0, 1, -1, 0, -1, 1, 0, 0, 0]
        }
        for case, reference in cases.items():
            FIELD.set_field(case)
            assert FIELD.field == reference

    @staticmethod
    def test_get_field():
        cases = {
            # set_field input: get_field output
            "_XXOO_OX_": """
---------
|   X X |
| O O   |
| O X   |
---------
""",
            "XX_XOXOO_": """
---------
| X X   |
| X O X |
| O O   |
---------
""",
            "OX_XOOOXX": """
---------
| O X   |
| X O O |
| O X X |
---------
""",
            "_XO_OX___": """
---------
|   X O |
|   O X |
|       |
---------
"""
        }
        for case, reference in cases.items():
            FIELD.set_field(case)
            assert FIELD.get_field() == reference


class TestPlayer:

    @staticmethod
    def test_check():
        cases = {
            # level: check result
            "user": "user",
            "medium": "medium",
            "user2": "ValueError",
            "hard": "hard",
            "": "ValueError",
            "level": "ValueError",
            "noname": "ValueError",
            "User": "ValueError",
            "mediumM": "ValueError",
            "HARD": "ValueError"
        }
        player = tictactoe.Player("X", "user")
        for case, reference in cases.items():
            try:
                result = player._check(case)
            except ValueError:
                result = "ValueError"
            assert result == reference

    @staticmethod
    def manual_test_make_move():
        """
        Method was tested manually.
        Expected results:

        ---------
        |       |
        |       |
        |       |
        ---------
        Enter the coordinates: 2 2
        ---------
        |       |
        |   X   |
        |       |
        ---------
        Making move level "easy"
        ---------
        |       |
        |   X   |
        | O     |
        ---------
        Enter the coordinates:
        """
        return


class TestConcreteMove:

    @staticmethod
    def manual_test_user():
        TestMoveStrategy().manual_test_manually()

    @staticmethod
    def test_easy():
        TestMoveStrategy().test_randomly()

    @staticmethod
    def test_medium():
        cases = {
            # set_field input: field state after medium move
            "_XXOO_OX_": [1, 1, 1, -1, -1, 0, -1, 1, 0],
            "XX_XOXOO_": [1, 1, 1, 1, -1, 1, -1, -1, 0],
            "OX_XOOOXX": [-1, 1, 1, 1, -1, -1, -1, 1, 1],
            "_XO_OX___": [0, 1, -1, 0, -1, 1, 1, 0, 0]
        }
        for case, reference in cases.items():
            FIELD.set_field(case)
            CONCRETE.medium(1, FIELD)
            assert FIELD.field == reference

    @staticmethod
    def test_hard():
        # TODO
        cases = {
            # set_field input: number moves for winning
            "_X_XO__O_": [2, 3],
            "O________": [2, 3],
            "_________": [3, 4]
        }
        for case, reference in cases.items():
            FIELD.set_field(case)
            moves = 0
            while FIELD.__str__() != "O wins":
                CONCRETE.hard(-1, FIELD)
                moves += 1
            assert moves in reference


class TestMoveStrategy:

    @staticmethod
    def manual_test_manually():
        """
        Method was tested manually.
        Expected results:

        ---------
        |       |
        |       |
        | X     |
        ---------
        Enter the coordinates: 1 1
        This cell is occupied! Choose another one!
        Enter the coordinates: one
        You should enter numbers!
        Enter the coordinates: one three
        You should enter numbers!
        Enter the coordinates: 4 1
        Coordinates should be from 1 to 3!
        Enter the coordinates: 1 3
        ---------
        | X     |
        |       |
        | X     |
        ---------

        """
        return

    @staticmethod
    def test_randomly():
        cases = {
            # set_field input: number moves for winning
            "OX_XOOOXX": [1],
            "XX_XOXOO_": [1, 2],
            "_XXOO_OX_": [1, 2, 3],
            "_XO_OX___": [1, 2, 3, 4, 5],
            "_________": [1, 2, 3, 4, 5, 6, 7, 8, 9]
        }
        for case, reference in cases.items():
            FIELD.set_field(case)
            moves = 0
            while FIELD.__str__() != "O wins":
                STRATEGY.randomly(-1, FIELD)
                moves += 1
            assert moves in reference

    @staticmethod
    def test_minimax():
        # set_field input: best case (minimax output)
        cases = {
            ("_X_XO__O_", 4): [0, 3],
            ("X________", 8): [8, 3]
        }
        for case, reference in cases.items():
            field, depth = case
            FIELD.set_field(field)
            result = STRATEGY.minimax(1, FIELD, depth)
            assert result == reference

    @staticmethod
    def test_empties():
        cases = {
            # set_field input: indexes of the empty cells
            "OX_XOOOXX": [2],
            "XX_XOXOO_": [2, 8],
            "_XXOO_OX_": [0, 5, 8],
            "_XO_OX___": [0, 3, 6, 7, 8]
        }
        for case, reference in cases.items():
            FIELD.set_field(case)
            assert STRATEGY.empties(FIELD) == reference


def manual_test_main():
    pass


def test_computer_vs_computer():

    def game(palyer_x: str, player_o: str):
        FIELD.set_field("_________")
        player = {
            FIELD.sign_x: tictactoe.Player("X", palyer_x),
            FIELD.sign_o: tictactoe.Player("O", player_o)
        }
        turn = FIELD.sign_x
        while True:
            player[turn].make_move(FIELD)
            if FIELD.__str__() != "Game not finished":
                break
            turn = -turn
        return FIELD.__str__()

    cases = {
        # (player_x, player_o): who win
        # equally
        ("hard", "hard"): ("Draw"),
        ("easy", "easy"): ("Draw", "X wins", "O wins"),
        ("medium", "medium"): ("Draw", "X wins"),
        # easy vs ...
        ("easy", "medium"): ("Draw", "O wins"),
        ("easy", "hard"): ("Draw", "O wins"),
        # medium vs ...
        ("medium", "easy"): ("Draw", "X wins"),
        ("medium", "hard"): ("Draw", "O wins"),
        # hard vs ...
        ("hard", "easy"): ("X wins"),
        ("hard", "medium"): ("Draw", "X wins")
    }
    for case, reference in cases.items():
        assert game(case[0], case[1]) in reference
