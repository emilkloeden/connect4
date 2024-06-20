from connect4.exceptions import UnableToPerformActionError
from connect4.models.cell import Cell
from connect4.models.cellvalue import CellValue


class Column:
    cells: list[Cell | None]
    index: int = 0

    def __init__(self, cells: list[Cell] | None = None, index: int = 0):
        if cells is None:
            self.cells = [None for _ in range(6)]
        else:
            self.cells = cells

    @property
    def as_list(self) -> list[CellValue | None]:
        return [cell.value.value if cell else None for cell in self.cells]

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
