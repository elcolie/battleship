import pytest

from fleets.models import Fleet
from commons.tests import board
from fleets.utils import add_battleship, OutOceanException, add_submarine, NearShipException


def test_place_battleship_left_top_corner_vertical(board):
    add_battleship(board, 1, 1, vertical=True)
    assert 4 == Fleet.objects.filter(fleet_type=Fleet.FleetType.battleship, x_axis=1, occupied=True).count()


def test_place_battleship_left_top_corner_horizontal(board):
    add_battleship(board, 1, 1, vertical=False)
    assert 4 == Fleet.objects.filter(fleet_type=Fleet.FleetType.battleship, y_axis=1, occupied=True).count()


def test_place_battleship_left_bottom_vertical(board):
    """Expect raises an Exception"""
    with pytest.raises(OutOceanException):
        add_battleship(board, 1, 10, vertical=True)
    assert 0 == Fleet.objects.count()


def test_place_battleship_left_bottom_horizontal(board):
    add_battleship(board, 1, 10, vertical=False)
    assert 4 == Fleet.objects.filter(fleet_type=Fleet.FleetType.battleship, y_axis=10, occupied=True).count()


def test_place_battleship_right_top_vertical(board):
    add_battleship(board, 10, 1, vertical=True)
    assert 4 == Fleet.objects.filter(fleet_type=Fleet.FleetType.battleship, x_axis=10, occupied=True).count()


def test_place_battleship_at_right_top_horizontal(board):
    with pytest.raises(OutOceanException):
        add_battleship(board, 10, 1, vertical=False)
    assert 0 == Fleet.objects.count()


def test_place_battleship_at_right_bottom_vertical(board):
    with pytest.raises(OutOceanException):
        add_battleship(board, 10, 10, vertical=True)
    assert 0 == Fleet.objects.count()


def test_place_battleship_at_right_bottom_horizontal(board):
    with pytest.raises(OutOceanException):
        add_battleship(board, 10, 10, vertical=False)
    assert 0 == Fleet.objects.count()


def test_place_submarine_left_top_vertical(board):
    add_submarine(board, 1, 1, vertical=True)
    assert 1 == Fleet.objects.filter(occupied=True).count()


def test_place_submarine_left_top_horizontal(board):
    add_submarine(board, 1, 1, vertical=False)
    assert 1 == Fleet.objects.filter(occupied=True).count()


def test_place_submarine_right_bottom(board):
    add_submarine(board, 1, 1, vertical=False)
    assert 1 == Fleet.objects.filter(occupied=True).count()


'''Vertical/Horizontal surrounding'''


def test_submarine_surrounding_vertical_under(board):
    add_submarine(board, 5, 5, vertical=False)
    with pytest.raises(NearShipException):
        add_submarine(board, 5, 6, vertical=False)


def test_submarine_surrounding_vertical_upper(board):
    add_submarine(board, 5, 5, vertical=False)
    with pytest.raises(NearShipException):
        add_submarine(board, 5, 4, vertical=False)


def test_submarine_surrounding_horizontal_left(board):
    add_submarine(board, 5, 5, vertical=False)
    with pytest.raises(NearShipException):
        add_submarine(board, 4, 5, vertical=False)


def test_submarine_surrounding_horizontal_right(board):
    add_submarine(board, 5, 5, vertical=False)
    with pytest.raises(NearShipException):
        add_submarine(board, 6, 5, vertical=False)


'''Diagonal surrounding'''


def test_submarine_surrounding_up_left(board):
    add_submarine(board, 5, 5, vertical=False)
    with pytest.raises(NearShipException):
        add_submarine(board, 4, 4, vertical=False)


def test_submarine_surrounding_up_right(board):
    add_submarine(board, 5, 5, vertical=False)
    with pytest.raises(NearShipException):
        add_submarine(board, 6, 4, vertical=False)


def test_submarine_surrounding_down_left(board):
    add_submarine(board, 5, 5, vertical=False)
    with pytest.raises(NearShipException):
        add_submarine(board, 4, 6, vertical=False)


def test_submarine_surrounding_down_right(board):
    add_submarine(board, 5, 5, vertical=False)
    with pytest.raises(NearShipException):
        add_submarine(board, 6, 6, vertical=False)


def test_submarine_overlap_battle_ship(board):
    """
    X : submarine
    Y : battleship
    Alignment: XYYYY
    :param board:
    :return:
    """
    add_submarine(board, 5, 5, vertical=False)
    with pytest.raises(NearShipException):
        add_battleship(board, 5, 6, vertical=False)