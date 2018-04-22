import pytest
from django.contrib.auth.models import User
from model_mommy import mommy

from boards.models import Board
from fleets.models import Fleet


@pytest.fixture
def board(db):
    mbx = mommy.make(User, username='sarit')
    lullalab = mommy.make(User, username='tiras')
    return mommy.make(Board, defender=lullalab, attacker=mbx, is_done=False)


@pytest.fixture
def battleship(board):
    return {
        'board': board.id,
        'fleet_type': Fleet.FleetType.battleship,
        'vertical': False,
        'x_axis': 1,
        'y_axis': 1,
    }


@pytest.fixture
def cruiser1(board):
    return {
        'board': board.id,
        'fleet_type': Fleet.FleetType.cruiser,
        'vertical': False,
        'x_axis': 1,
        'y_axis': 4,
    }


@pytest.fixture
def cruiser2(board):
    return {
        'board': board.id,
        'fleet_type': Fleet.FleetType.cruiser,
        'vertical': True,
        'x_axis': 10,
        'y_axis': 2,
    }


@pytest.fixture
def destroyer1(board):
    return {
        'board': board.id,
        'fleet_type': Fleet.FleetType.destroyer,
        'vertical': False,
        'x_axis': 2,
        'y_axis': 6,
    }


@pytest.fixture
def destroyer2(board):
    return {
        'board': board.id,
        'fleet_type': Fleet.FleetType.destroyer,
        'vertical': True,
        'x_axis': 4,
        'y_axis': 8,
    }


@pytest.fixture
def destroyer3(board):
    return {
        'board': board.id,
        'fleet_type': Fleet.FleetType.destroyer,
        'vertical': True,
        'x_axis': 6,
        'y_axis': 5,
    }


@pytest.fixture
def submarine1(board):
    return {
        'board': board.id,
        'fleet_type': Fleet.FleetType.submarine,
        'vertical': False,
        'x_axis': 7,
        'y_axis': 8,
    }


@pytest.fixture
def submarine2(board):
    return {
        'board': board.id,
        'fleet_type': Fleet.FleetType.submarine,
        'vertical': False,
        'x_axis': 8,
        'y_axis': 4,
    }


@pytest.fixture
def submarine3(board):
    return {
        'board': board.id,
        'fleet_type': Fleet.FleetType.submarine,
        'vertical': False,
        'x_axis': 8,
        'y_axis': 6,
    }


@pytest.fixture
def submarine4(board):
    return {
        'board': board.id,
        'fleet_type': Fleet.FleetType.submarine,
        'vertical': False,
        'x_axis': 10,
        'y_axis': 8,
    }
