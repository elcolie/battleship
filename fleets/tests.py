import pytest

from fleets.models import Fleet
from commons.tests import board
from fleets.utils import add_battleship, OutOceanException, add_submarine


def test_place_battleship_left_top_corner_vertical(board):
    add_battleship(board, 1, 1, vertical=True)
    assert 4 == Fleet.objects.filter(fleet_type=Fleet.FleetType.battleship, x_axis=1,occupied=True).count()


def test_place_battleship_left_top_corner_horizontal(board):
    add_battleship(board, 1, 1, vertical=False)
    assert 4 == Fleet.objects.filter(fleet_type=Fleet.FleetType.battleship, y_axis=1,occupied=True).count()


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
    assert 4 == Fleet.objects.filter(fleet_type=Fleet.FleetType.battleship, x_axis=10 ,occupied=True).count()


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
