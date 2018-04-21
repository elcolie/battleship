import pytest

from fleets.models import Fleet, OutOceanException
from commons.tests import board


def test_place_battleship_left_top_corner_vertical(board):
    Fleet.objects.add_battleship(board, 1, 1, vertical=True)
    assert 4 == Fleet.objects.filter(fleet_type=Fleet.FleetType.battleship, x_axis=1).count()


def test_place_battleship_left_top_corner_horizontal(board):
    Fleet.objects.add_battleship(board, 1, 1, vertical=False)
    assert 4 == Fleet.objects.filter(fleet_type=Fleet.FleetType.battleship, y_axis=1).count()


def test_place_battleship_left_bottom_vertical(board):
    """Expect raises an Exception"""
    with pytest.raises(OutOceanException):
        Fleet.objects.add_battleship(board, 1, 10, vertical=True)
    assert 0 == Fleet.objects.count()


def test_place_battleship_left_bottom_horizontal(board):
    Fleet.objects.add_battleship(board, 1, 10, vertical=False)
    assert 4 == Fleet.objects.filter(fleet_type=Fleet.FleetType.battleship, y_axis=10).count()


def test_place_battleship_right_top_vertical(board):
    Fleet.objects.add_battleship(board, 10, 1, vertical=True)
    assert 4 == Fleet.objects.filter(fleet_type=Fleet.FleetType.battleship, x_axis=10).count()


def test_place_battleship_at_right_top_horizontal(board):
    with pytest.raises(OutOceanException):
        Fleet.objects.add_battleship(board, 10, 1, vertical=False)
    assert 0 == Fleet.objects.count()


def test_place_battleship_at_right_bottom_vertical(board):
    with pytest.raises(OutOceanException):
        Fleet.objects.add_battleship(board, 10, 10, vertical=True)
    assert 0 == Fleet.objects.count()


def test_place_battleship_at_right_bottom_horizontal(board):
    with pytest.raises(OutOceanException):
        Fleet.objects.add_battleship(board, 10, 10, vertical=False)
    assert 0 == Fleet.objects.count()


def test_place_submarine_left_top_vertical(board):
    Fleet.objects.add_submarine(board, 1, 1, vertical=True)
    assert 1 == Fleet.objects.count()


def test_place_submarine_left_top_horizontal(board):
    Fleet.objects.add_submarine(board, 1, 1, vertical=False)
    assert 1 == Fleet.objects.count()


def test_place_submarine_right_bottom(board):
    Fleet.objects.add_submarine(board, 1, 1, vertical=False)
    assert 1 == Fleet.objects.count()
