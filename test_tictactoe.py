""" tests by PyTest """

import tictactoe


class TestPlayField:

    def test__repr__(self):
        cases = {
            "XXXOO_OX_": tictactoe.PlayField.sign_x * 3,
            "XX_XOXOOO": tictactoe.PlayField.sign_o * 3,
            "OXXXOOOXX": tictactoe.PlayField.status_draw,
            "_XO_OXX__": tictactoe.PlayField.status_game
        }
        play_field = tictactoe.PlayField()
        for case, reference in cases.items():
            play_field.set_field(case)
            assert play_field.__repr__() == reference

    def test__str__(self):
        cases = {
            "XXXOO_OX_": "X wins",
            "XX_XOXOOO": "O wins",
            "OXXXOOOXX": "Draw",
            "_XO_OXX__": "Game not finished"
        }
        play_field = tictactoe.PlayField()
        for case, reference in cases.items():
            play_field.set_field(case)
            assert play_field.__str__() == reference

    def test_set_field(self):
        cases = {
            "_XXOO_OX_": [0, 1, 1, -1, -1, 0, -1, 1, 0],
            "XX_XOXOO_": [1, 1, 0, 1, -1, 1, -1, -1, 0],
            "OX_XOOOXX": [-1, 1, 0, 1, -1, -1, -1, 1, 1],
            "_XO_OX___": [0, 1, -1, 0, -1, 1, 0, 0, 0]
        }
        play_field = tictactoe.PlayField()
        for case, reference in cases.items():
            play_field.set_field(case)
            assert play_field.matrix == reference

    def test_get_field(self):
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
        play_field = tictactoe.PlayField()
        for case, reference in cases.items():
            play_field.set_field(case)
            assert play_field.get_field() == reference


class TestMove:

    def test_manually(self, capsys):
        """ TODO """
        pass
