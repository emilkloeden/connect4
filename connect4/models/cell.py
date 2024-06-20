from connect4.models.cellvalue import CellValue


class Cell:
    value: CellValue

    def __init__(self, value: CellValue | None = None) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value.value) if self.value else " "
