from connect4.models import CellValue, Game, Grid


def main():
    game = Game()
    grid = game.grid
    p1, p2 = game.players
    p1.place(0)

    p2.place(0)

    p1.place(0)

    p2.place(2)


if __name__ == "__main__":
    main()
