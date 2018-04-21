import pytest

from fleets.models import Fleet, OutOceanException
from commons.tests import board


def test_place_submarine_at_corner(board):
    pass


def test_place_submarine_at_middle(board):
    pass


def test_place_battleship_at_left_top_corner(board):
    Fleet.objects.add_ship(board, 1, 1, vertical=True)
    assert 4 == Fleet.objects.filter(fleet_type=Fleet.FleetType.battleship, x_axis=1).count()


def test_place_battle_at_left_bottown(board):
    """Expect raises an Exception"""
    with pytest.raises(OutOceanException):
        Fleet.objects.add_ship(board, 1, 10, vertical=True)
    assert 0 == Fleet.objects.count()

def test_place_battle_ship_at_middle(board):
    pass
