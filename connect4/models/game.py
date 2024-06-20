from __future__ import annotations
from pathlib import Path

from connect4.exceptions import UnableToPerformActionError
from connect4.models.cellvalue import CellValue
from connect4.models.column import Column
from connect4.models.events import Event, Play, parse_event
from connect4.models.gamestate import GameState


class Game:
    state: GameState
    grid: Grid
    players: tuple[Player, Player]
    events: list[Event]
    event_log: Path = Path("connect4.game")

    def __init__(self) -> None:
        self.state = GameState.O_TURN
        self.grid = Grid(self)
        self.players = (
            Player(CellValue.O, self),
            Player(CellValue.X, self),
        )
        self.events = []

    def load_events(self) -> None:
        try:
            text = self.event_log.read_text()
            self.events = [parse_event(line) for line in text.splitlines()]
        except FileNotFoundError:
            self.events = []

    # TODO
    def has_player_won_horizontally(self, player: Player) -> bool:
        # number_to_win = 4
        # grid = self.grid
        # matrix = grid.as_matrix
        # for i in range(grid.NUM_COLUMNS):
        #     for j in range(grid.NUM_ROWS):
        #         print(i, j)
        return False

    # TODO
    def has_player_won_vertically(self, player: Player) -> bool:
        number_to_win = 4
        grid = self.grid
        matrix = grid.as_matrix
        for column in matrix:
            for i in range(grid.NUM_ROWS - number_to_win):
                if all(
                    map(
                        lambda cell: cell == player.value.value,
                        column[i : i + number_to_win],
                    )
                ):
                    return True

        return False

    # TODO
    def has_player_won_top_left_to_bottom_right(self, player: Player) -> bool:
        return False

    # TODO
    def has_player_won_top_right_to_bottom_left(self, player: Player) -> bool:
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
        has_won = self.has_player_won(x)
        if has_won:
            self.state = GameState.X_WON
        return has_won

    def has_o_won(self) -> bool:
        o, _x = self.players
        has_won = self.has_player_won(o)
        if has_won:
            self.state = GameState.O_WON
        return has_won

    def is_it_a_draw(self):
        return all([column.is_full() for column in self.grid.columns])

    def is_game_over(self):
        return self.has_x_won() or self.has_o_won() or self.is_it_a_draw()

    def post_play(self):
        if self.is_game_over():
            self.print_result_message()
            print()
        else:
            self.swap_turns()

    def print_result_message(self):
        if self.state == GameState.X_WON:
            print("\n   X WINS!!!\n")
        elif self.state == GameState.O_WON:
            print("\n   O WINS!!!\n")
        elif self.state == GameState.DRAW:
            print("\n GAME ENDS IN A DRAW\n")

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


class Grid:
    columns: list[Column]
    game: Game
    NUM_COLUMNS = 7
    NUM_ROWS = 6

    def __init__(self, game: Game):
        self.game = game
        self.columns = [Column(index=i) for i in range(self.NUM_COLUMNS)]

    @property
    def as_matrix(self) -> list[list[CellValue | None]]:
        return [column.as_list for column in self.columns]

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


class Player:
    value: CellValue
    game: Game

    def __init__(self, value: CellValue, game: Game) -> None:
        self.game = game
        self.value = value

    def place(self, col_index):
        self.game.grid.place(col_index, self.value)
