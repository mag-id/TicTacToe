""" tests by PyTest """

import TicTacToe as tictactoe

FIELD = tictactoe.PlayField()
MOVE = tictactoe.Move()


class TestPlayField:

    @staticmethod
    def test__repr__():
        cases = {
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
            "_XXOO_OX_": [0, 1, 1, -1, -1, 0, -1, 1, 0],
            "XX_XOXOO_": [1, 1, 0, 1, -1, 1, -1, -1, 0],
            "OX_XOOOXX": [-1, 1, 0, 1, -1, -1, -1, 1, 1],
            "_XO_OX___": [0, 1, -1, 0, -1, 1, 0, 0, 0]
        }
        for case, reference in cases.items():
            FIELD.set_field(case)
            assert FIELD.matrix == reference

    @staticmethod
    def test_get_field():
        cases = {
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


class TestMove:

    @staticmethod
    def test_manually():
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
                MOVE.randomly("O", FIELD)
                moves += 1
            assert moves in reference

    @staticmethod
    def test_empties():
        cases = {
            "OX_XOOOXX": [2],
            "XX_XOXOO_": [2, 8],
            "_XXOO_OX_": [0, 5, 8],
            "_XO_OX___": [0, 3, 6, 7, 8]
        }
        for case, reference in cases.items():
            FIELD.set_field(case)
            assert MOVE._empties(FIELD) == reference


class TestPlayer:

    @staticmethod
    def test_check():
        cases = {
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
    def test_making_move():
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
