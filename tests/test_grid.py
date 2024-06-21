from connect4.models.game import Game


def test_vertical_solve():
    game = Game()
    o, x = game.players
    assert not game.has_player_won_vertically(x)
    assert not game.has_player_won_vertically(o)
    o.place(0)
    assert not game.has_player_won_vertically(x)
    assert not game.has_player_won_vertically(o)
    x.place(1)
    assert not game.has_player_won_vertically(x)
    assert not game.has_player_won_vertically(o)
    o.place(0)
    assert not game.has_player_won_vertically(x)
    assert not game.has_player_won_vertically(o)
    x.place(1)
    assert not game.has_player_won_vertically(x)
    assert not game.has_player_won_vertically(o)
    o.place(0)
    assert not game.has_player_won_vertically(x)
    assert not game.has_player_won_vertically(o)
    x.place(1)
    assert not game.has_player_won_vertically(x)
    assert not game.has_player_won_vertically(o)
    o.place(0)
    assert not game.has_player_won_vertically(x)
    assert game.has_player_won_vertically(o)


def test_horizontal_solve():
    game = Game()
    o, x = game.players
    assert not game.has_player_won_horizontally(x)
    assert not game.has_player_won_horizontally(o)
    o.place(3)
    assert not game.has_player_won_horizontally(x)
    assert not game.has_player_won_horizontally(o)
    x.place(3)
    assert not game.has_player_won_horizontally(x)
    assert not game.has_player_won_horizontally(o)
    o.place(2)
    assert not game.has_player_won_horizontally(x)
    assert not game.has_player_won_horizontally(o)
    x.place(2)
    assert not game.has_player_won_horizontally(x)
    assert not game.has_player_won_horizontally(o)
    o.place(1)
    assert not game.has_player_won_horizontally(x)
    assert not game.has_player_won_horizontally(o)
    x.place(1)
    assert not game.has_player_won_horizontally(x)
    assert not game.has_player_won_horizontally(o)
    o.place(4)
    assert not game.has_player_won_horizontally(x)
    assert game.has_player_won_horizontally(o)


def test_diagonal_bottom_left_to_top_right():
    game = Game()
    o, x = game.players

    assert not game.has_player_won_bottom_left_to_top_right(x)
    assert not game.has_player_won_bottom_left_to_top_right(o)

    o.place(0)
    x.place(1)
    o.place(1)
    x.place(2)
    o.place(3)
    x.place(2)
    o.place(2)
    x.place(3)
    o.place(3)
    x.place(4)
    o.place(3)
    assert not game.has_player_won_bottom_left_to_top_right(x)
    assert game.has_player_won_bottom_left_to_top_right(o)


def test_diagonal_bottom_right_to_top_left():
    game = Game()
    o, x = game.players

    assert not game.has_player_won_bottom_right_to_top_left(x)
    assert not game.has_player_won_bottom_right_to_top_left(o)

    o.place(0)
    x.place(0)
    o.place(0)
    x.place(0)
    o.place(1)
    x.place(3)
    o.place(1)
    x.place(1)
    o.place(2)
    x.place(2)
    assert not game.has_player_won_bottom_right_to_top_left(o)
    assert game.has_player_won_bottom_right_to_top_left(x)
