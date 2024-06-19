import argparse
from connect4.models import Game
from connect4.models.events import Play


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("player", choices=("O", "X"))
    parser.add_argument("column", type=int_range(0, 6))
    return parser.parse_args()


def int_range(min_value: int, max_value: int):
    def validator(value):
        try:
            int_value = int(value)
        except TypeError:
            raise argparse.ArgumentTypeError(
                f"Value must be an integer between {min_value} and {max_value}"
            )
        if int_value < min_value or int_value > max_value:
            raise argparse.ArgumentTypeError(
                f"Value must be an integer between {min_value} and {max_value}"
            )
        return int_value

    return validator


def main():
    args = parse_args()
    game = Game()
    grid = game.grid

    game.load_events()
    play = Play(args.player, args.column)
    game.events.append(play)
    game.play_events()
    game.save_events()
    print(grid)


if __name__ == "__main__":
    main()
