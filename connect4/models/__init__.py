from __future__ import annotations
import enum
from pathlib import Path

from connect4.models.events import Event, Play, parse_event


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
    events: list[Event]
    event_log: Path = Path("connect4.game")

    def __init__(self) -> None:
        self.state = GameState.O_TURN
        self.grid = Grid(self)
        self.players = (Player(CellValue.O, self), Player(CellValue.X, self))
        self.events = []

    def load_events(self) -> None:
        try:
            text = self.event_log.read_text()
            self.events = [parse_event(line) for line in text.splitlines()]
        except FileNotFoundError:
            self.events = []

    # TODO
    def has_player_won_horizontally(player) -> bool:
        return False

    # TODO
    def has_player_won_vertically(player) -> bool:
        return False

    # TODO
    def has_player_won_top_left_to_bottom_right(player) -> bool:
        return False

    # TODO
    def has_player_won_top_right_to_bottom_left(player) -> bool:
        return False

    def has_player_won(self, player: Player) -> bool:
        return (
            self.has_player_won_horizontally(player)
            or self.has_player_won_vertically(player)
            or self.has_player_won_top_left_to_bottom_right(player)
            or self.has_player_won_top_right_to_bottom_left(player)
        )

    def has_x_won(self) -> bool:
        _, x = self.players
        return self.has_player_won(x)

    def has_o_won(self) -> bool:
        o, _x = self.players
        return self.has_player_won(o)

    # TODO
    def is_it_a_draw(self):
        return False

    def is_game_over(self):
        return self.has_x_won() or self.has_o_won() or self.is_it_a_draw()

    def post_play(self):
        if not self.is_game_over():
            self.swap_turns()

    def swap_turns(self):
        if self.state == GameState.O_TURN:
            self.state = GameState.X_TURN
        elif self.state == GameState.X_TURN:
            self.state = GameState.O_TURN

    def is_play_valid(self, play: Play) -> None:
        return self.it_is_the_correct_players_turn(play) and self.the_column_is_valid(
            play
        )

    def it_is_the_correct_players_turn(self, play: Play) -> bool:
        return (play.player == "X" and self.state == GameState.X_TURN) or (
            play.player == "O" and self.state == GameState.O_TURN
        )
        # TODO: Consider adding handling of game over states

    def the_column_is_valid(self, play: Play) -> bool:
        return 0 <= play.column <= 6 and not self.grid.columns[play.column].is_full()

    def play_events(self) -> None:
        for event in self.events:
            if isinstance(event, Play):
                if self.is_play_valid(event):
                    self.play_a_play(event)
                    self.post_play()
                else:
                    self.bring_things_to_a_crashing_halt()

    def bring_things_to_a_crashing_halt(self):
        raise UnableToPerformActionError("That just can't happen")

    def save_events(self) -> None:
        text = "\n".join(str(event) for event in self.events)
        self.event_log.write_text(text)

    def play_a_play(self, play: Play) -> None:
        o, x = self.players
        if play.player == "O":
            o.place(play.column)
        elif play.player == "X":
            x.place(play.column)

    def check_end_game(self):
        return False


class Player:
    value: CellValue
    game: Game

    def __init__(self, value, game) -> None:
        self.game = game
        self.value = value

    def place(self, col_index):
        self.game.grid.place(col_index, self.value)


class Grid:
    columns: list[Column]
    game: Game

    def __init__(self, game: Game, columns: list[Column] | None = None):
        self.game = game
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
        if (self.game.state == GameState.O_TURN and CellValue.O) or (
            self.game.state == GameState.X_TURN and CellValue.X
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
                # self.game.check_end_game()
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

    def is_full(self) -> bool:
        self.cells.count(None) == 0

    def append(self, value: CellValue):
        try:
            next_slot = self.cells.index(None)
        except ValueError:
            raise UnableToPerformActionError(
                f"Cannot append to column {self.index}, full."
            )
        self.cells[next_slot] = Cell(value)

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
