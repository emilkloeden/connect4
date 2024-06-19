from __future__ import annotations
import enum


class UnableToPerformActionError(ValueError):
    def __init__(self, message: str | None):
        self.message = message
        super().__init__(message)


class GameState(enum.Enum):
    O_TURN = "O_TURN"
    X_TURN = "X_TURN"
    O_WON = "O_WON"
    X_WON = "X_WON"


class Game:
    state: GameState
    grid: Grid
    players: tuple[Player, Player]

    def __init__(self) -> None:
        self.state = GameState.O_TURN
        self.grid = Grid(self)
        self.players = (Player(CellValue.O, self), Player(CellValue.X, self))

    def check_end_game(self):
        return False


class Player:
    value: CellValue
    game: Game

    def place(self, col_index):
        self.game.place(col_index, self.value)


class Grid:
    columns: list[Column]
    game: Game

    def __init__(self, game: Game, columns: list[Column] | None = None):
        if columns is None:
            self.columns = [Column(index=i) for i in range(7)]
        else:
            self.columns = columns

    def __getitem__(self, index):
        return self.columns[index]

    def __setitem__(self, index, value):
        self.columns[index] = value

    def __str__(self) -> str:
        rotated_grid_str = "\n".join(
            " ".join(str(cell) if cell else " " for cell in row)[::-1]
            for row in zip(*self.columns)
        )[::-1]
        column_numbers_str = " ".join(str(i) for i in range(len(self.columns)))
        return f"{rotated_grid_str}\n{column_numbers_str}"

    def place(self, col_index: int, value: CellValue) -> None:
        if (self.game.game_state == GameState.O_TURN and CellValue.O) or (
            self.game_state == GameState.X_TURN and CellValue.X
        ):
            if not isinstance(col_index, int):
                raise TypeError(
                    f"Invalid type passed for column index {type(col_index)}"
                )
            if not 0 <= col_index < len(self.columns):
                raise ValueError(f"Invalid location to place CellValue {col_index}")
            if not isinstance(value, CellValue):
                raise TypeError("Must use a valid CellValue when placing")
            try:
                self.columns[col_index].append(value)
                self.game.check_end_game()
            except UnableToPerformActionError:
                raise
        # TODO: Properly handle endgame states
        else:
            raise UnableToPerformActionError(
                f"Wrong player's turn. Currently {self.game.state}."
            )


class Column:
    cells: list[Cell | None]
    index: int = 0

    def __init__(self, cells: list[Cell] | None = None, index: int = 0):
        if cells is None:
            self.cells = [None for _ in range(6)]
        else:
            self.cells = cells

    def append(self, value: CellValue):
        try:
            index = self.cells.index(None)
        except ValueError:
            raise UnableToPerformActionError(
                f"Cannot append to column {self.index}, full."
            )
        self.cells[index] = Cell(value)

    def __getitem__(self, index):
        return self.cells[index]

    def __setitem__(self, index, value):
        self.cells[index] = value

    def __iter__(self):
        return iter(self.cells)

    def __str__(self) -> str:
        return " ".join(str(cell) if cell else "m" for cell in self.cells)


class Cell:
    value: CellValue

    def __init__(self, value: CellValue | None = None) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value.value) if self.value else " "


class CellValue(enum.Enum):
    X = "X"
    O = "O"
