from dataclasses import dataclass
from typing import Literal


@dataclass
class Play:
    player: Literal["X"] | Literal["O"]
    column: int

    def __str__(self) -> str:
        return f"P{self.player}{self.column}"


def parse_event(line: str) -> Play:
    if line.startswith("P"):
        player = line[1]
        column = int(line[2])
        return Play(player, column)


Event = Play
