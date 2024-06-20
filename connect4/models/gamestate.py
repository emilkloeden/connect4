import enum


class GameState(enum.Enum):
    O_TURN = "O_TURN"
    X_TURN = "X_TURN"
    O_WON = "O_WON"
    X_WON = "X_WON"
    DRAW = "DRAW"
