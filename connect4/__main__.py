from connect4.models import CellValue, Grid


def main():
    grid = Grid()
    grid.place(0, CellValue.X)
    grid.place(0, CellValue.X)
    grid.place(0, CellValue.X)
    grid.place(0, CellValue.X)
    grid.place(0, CellValue.X)
    grid.place(0, CellValue.X)
    grid.place(0, CellValue.X)  # noqa: F821
    # grid.place(0, CellValue.X)
    # grid.place(0, CellValue.O)
    # grid.place(1, CellValue.O)
    print(grid)


if __name__ == "__main__":
    main()
