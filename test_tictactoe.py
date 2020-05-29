""" tests by PyTest """

import tictactoe

FIELD = tictactoe.PlayField()
STRATEGY = tictactoe.MoveStrategy()
CONCRETE = tictactoe.ConcreteMove()


class TestPlayField:

    @staticmethod
    def test_get_status_code():
    # expected get_status_code output: current PlayField.cells state
        cases = {
            +3: [1, 1, 1, -1, -1, 0, -1, 1, 0],
            -3: [1, 1, 0, 1, -1, 1, -1, -1, -1],
            0: [-1, 1, 1, 1, -1, -1, -1, 1, 1],
            9: [0, 1, -1, 0, -1, 1, 1, 0, 0]
        }
        for reference, case in cases.items():
            FIELD.cells = case
            assert FIELD.get_status_code() == reference

    @staticmethod
    def test_get_output():
        # expected get_output output: current PlayField.cells state
        cases = {
            """
---------
|   X X |
| O O   |
| O X   |
---------
""": [0, 1, 1, -1, -1, 0, -1, 1, 0],
            """
---------
| X X   |
| X O X |
| O O   |
---------
""": [1, 1, 0, 1, -1, 1, -1, -1, 0],
            """
---------
| O X   |
| X O O |
| O X X |
---------
""": [-1, 1, 0, 1, -1, -1, -1, 1, 1],
            """
---------
|   X O |
|   O X |
|       |
---------
""": [0, 1, -1, 0, -1, 1, 0, 0, 0]
        }
        for reference, case in cases.items():
            FIELD.cells = case
            assert FIELD.get_output() == reference


class TestPlayer:

    @staticmethod
    def test_check():
        cases = {
            # input level: check expected result
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


class TestConcreteMove:

    @staticmethod
    def test_medium():
        cases = [
            # current cells state: cells state after medium move
            ([0, 1, 1, -1, -1, 0, -1, 1, 0], [1, 1, 1, -1, -1, 0, -1, 1, 0]),
            ([1, 1, 0, 1, -1, 1, -1, -1, 0], [1, 1, 1, 1, -1, 1, -1, -1, 0]),
            ([-1, 1, 0, 1, -1, -1, -1, 1, 1], [-1, 1, 1, 1, -1, -1, -1, 1, 1]),
            ([0, 1, -1, 0, -1, 1, 0, 0, 0], [0, 1, -1, 0, -1, 1, 1, 0, 0])
        ]
        for case, reference in cases:
            FIELD.cells = case
            CONCRETE.medium(1, FIELD)
            assert FIELD.cells == reference

    @staticmethod
    def test_hard():
        # current cells state, expected sum of the cells
        case, reference = [0, 0, 0, 0, 0, 0, 0, 0, 0], 1
        FIELD.cells = case
        CONCRETE.hard(1, FIELD)
        assert sum(FIELD.cells) == reference


class TestMoveStrategy:

    @staticmethod
    def test_randomly():
        # number of moves for winning: expected win cells state
        cases = {
            (1,): [-1, 1, 0, 1, -1, -1, -1, 1, 1],
            (1, 2): [1, 1, 0, 1, -1, 1, -1, -1, 1],
            (1, 2, 3): [0, 1, 1, -1, -1, 0, -1, 1, 0],
            (1, 2, 3, 4, 5): [0, 1, -1, 0, -1, 1, 0, 0, 0],
            (1, 2, 3, 4, 5, 6, 7, 8, 9): [0, 0, 0, 0, 0, 0, 0, 0, 0]
        }
        for reference, case in cases.items():
            FIELD.cells = case
            moves = 0
            while FIELD.get_status_code() != tictactoe.O_WINS:
                STRATEGY.randomly(-1, FIELD)
                moves += 1
            assert moves in reference

    @staticmethod
    def test_minimax():
        # current cells state, depth, best case (minimax output)
        cases = [
            ([0, 1, 0, 1, -1, 0, 0, -1, 0], 4, [0, 3]),
            ([1, 0, 0, 0, 0, 0, 0, 0, 0], 8, [8, 3])
        ]
        for case, depth, reference in cases:
            FIELD.cells = case
            result = STRATEGY.minimax(1, FIELD, depth)
            assert result == reference

    @staticmethod
    def test_empty_cells():
        # current cells state, expected indexes of the empty cells
        cases = [
            ([-1, 1, 0, 1, -1, -1, -1, 1, 1], [2]),
            ([1, 1, 0, 1, -1, 1, -1, -1, 0], [2, 8]),
            ([0, 1, 1, -1, -1, 0, -1, 1, 0], [0, 5, 8]),
            ([0, 1, -1, 0, -1, 1, 0, 0, 0], [0, 3, 6, 7, 8])
        ]
        for case, reference in cases:
            FIELD.cells = case
            assert STRATEGY.empty_cells(FIELD) == reference


def test_computer_vs_computer():

    def game(palyer_x: str, player_o: str):
        FIELD.cells = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        player = {
            tictactoe.X_CELL: tictactoe.Player("X", palyer_x),
            tictactoe.O_CELL: tictactoe.Player("O", player_o)
        }
        turn = tictactoe.X_CELL
        while True:
            player[turn].make_move(FIELD)
            if FIELD.get_status_code() != tictactoe.NOT_FINISHED:
                break
            turn = -turn
        character = tictactoe.DECODE[turn]
        return "Draw" if not FIELD.get_status_code() else f"{character} wins"

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
