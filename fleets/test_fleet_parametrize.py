"""
Try new approach. Since I have time.
Test placing the fleets with parametrized values.
Beside the setup overhead. Coding style is `django class based TestCase`!
"""
import typing

import pytest
from django.conf import settings
from django.contrib.auth.models import User
from djchoices import ChoiceItem
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from boards.models import Board
from fleets.models import Fleet


def pytest_generate_tests(metafunc):
    # called once per each test function
    funcarglist = metafunc.cls.params[metafunc.function.__name__]
    argnames = sorted(funcarglist[0])
    metafunc.parametrize(argnames, [[funcargs[name] for name in argnames]
                                    for funcargs in funcarglist])


pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestFleetPlacement:
    params = {
        'test_boundary': [
            {
                'fleet_type': Fleet.FleetType.battleship,
                'x_axis': 1,
                'y_axis': 1,
                'vertical': False,
                'result': 4,
            },
            {
                'fleet_type': Fleet.FleetType.battleship,
                'x_axis': settings.OCEAN_SIZE,
                'y_axis': 1,
                'vertical': False,
                'result': 0,
            },
            {
                'fleet_type': Fleet.FleetType.battleship,
                'x_axis': settings.OCEAN_SIZE - 1,
                'y_axis': 1,
                'vertical': False,
                'result': 0,
            },
            {
                'fleet_type': Fleet.FleetType.battleship,
                'x_axis': settings.OCEAN_SIZE - 2,
                'y_axis': 1,
                'vertical': False,
                'result': 0,
            },
            {
                'fleet_type': Fleet.FleetType.battleship,
                'x_axis': settings.OCEAN_SIZE - 3,
                'y_axis': 1,
                'vertical': False,
                'result': 4,
            },
        ],
        'test_over_quota': [
            {
                'battleships': [
                    {
                        'fleet_type': Fleet.FleetType.battleship,
                        'vertical': False,
                        'x_axis': 1,
                        'y_axis': 1,
                    },
                    {
                        'fleet_type': Fleet.FleetType.battleship,
                        'vertical': False,
                        'x_axis': 4,
                        'y_axis': 4,
                    }],
                'cruisers': [],
                'destroyers': [],
                'submarines': [],
            },
            {
                'battleships': [],
                'cruisers': [
                    {
                        'fleet_type': Fleet.FleetType.cruiser,
                        'vertical': False,
                        'x_axis': 1,
                        'y_axis': 3,
                    },
                    {
                        'fleet_type': Fleet.FleetType.cruiser,
                        'vertical': True,
                        'x_axis': 9,
                        'y_axis': 2,
                    },
                    {
                        'fleet_type': Fleet.FleetType.cruiser,
                        'vertical': False,
                        'x_axis': 5,
                        'y_axis': 8,
                    }
                ],
                'destroyers': [],
                'submarines': [],
            },
            {
                'battleships': [],
                'cruisers': [],
                'destroyers': [
                    {
                        'fleet_type': Fleet.FleetType.destroyer,
                        'vertical': False,
                        'x_axis': 2,
                        'y_axis': 5,
                    },
                    {
                        'fleet_type': Fleet.FleetType.destroyer,
                        'vertical': True,
                        'x_axis': 5,
                        'y_axis': 4,
                    },
                    {
                        'fleet_type': Fleet.FleetType.destroyer,
                        'vertical': True,
                        'x_axis': 3,
                        'y_axis': 7,
                    },
                    {
                        'fleet_type': Fleet.FleetType.destroyer,
                        'vertical': False,
                        'x_axis': 4,
                        'y_axis': 10,
                    },
                ],
                'submarines': [],
            },
            {
                'battleships': [],
                'cruisers': [],
                'destroyers': [],
                'submarines': [
                    {
                        'fleet_type': Fleet.FleetType.submarine,
                        'vertical': False,
                        'x_axis': 6,
                        'y_axis': 7,
                    },
                    {
                        'fleet_type': Fleet.FleetType.submarine,
                        'vertical': False,
                        'x_axis': 7,
                        'y_axis': 3,
                    },
                    {
                        'fleet_type': Fleet.FleetType.submarine,
                        'vertical': False,
                        'x_axis': 7,
                        'y_axis': 5,
                    },
                    {
                        'fleet_type': Fleet.FleetType.submarine,
                        'vertical': False,
                        'x_axis': 9,
                        'y_axis': 7,
                    },
                    {
                        'fleet_type': Fleet.FleetType.submarine,
                        'vertical': False,
                        'x_axis': 10,
                        'y_axis': 10,
                    },
                ],
            }
        ],
        'test_placed': [
            {
                'existing_fleets': [
                    {
                        'fleet_type': Fleet.FleetType.battleship,
                        'x_axis': 1,
                        'y_axis': 1,
                        'vertical': False,
                    }
                ],
                'new_ships': [
                    {
                        'fleet_type': Fleet.FleetType.cruiser,
                        'x_axis': 4,
                        'y_axis': 3,
                        'vertical': False,
                    }
                ],
                'expected_result': {
                    'battleship_qty': 1,
                    'cruiser_qty': 1,
                }
            },
        ],
    }

    def create_board(self):
        defender, created = User.objects.get_or_create(username='elcolie', first_name='sarit', last_name='ritwiriune')
        attacker, created = User.objects.get_or_create(username='john', first_name='john', last_name='connor')
        board, created = Board.objects.get_or_create(defender=defender, attacker=attacker, is_done=False)

        client = APIClient()
        url = reverse('api:fleet-list')

        return (client, url, board)

    def test_placed(self, existing_fleets: typing.List[typing.Dict], new_ships: typing.Dict,
                    expected_result: typing.Dict[str, int]):
        client, url, board = self.create_board()
        for fleet in existing_fleets:
            fleet['board'] = board.id
            client.post(url, data=fleet, format='json')
        for new_ship in new_ships:
            new_ship['board'] = board.id
            client.post(url, data=new_ship, format='json')
        assert expected_result.get('battleship_qty') == Fleet.objects.filter(
            fleet_type=Fleet.FleetType.battleship).count() / settings.BATTLESHIP_SIZE
        assert expected_result.get('cruiser_qty') == Fleet.objects.filter(
            fleet_type=Fleet.FleetType.cruiser).count() / settings.CRUISER_SIZE

    def test_boundary(self, fleet_type, x_axis, y_axis, vertical, result):
        client, url, board = self.create_board()
        data = {
            'board': board.id,
            'fleet_type': fleet_type,
            'vertical': vertical,
            'x_axis': x_axis,
            'y_axis': y_axis,
        }
        client.post(url, data=data, format='json')
        assert result == Fleet.objects.filter(fleet_type=fleet_type).count()

    def test_over_quota(
            self,
            battleships: typing.List[typing.Dict[str, typing.Union[str, bool, int]]],
            cruisers: typing.List[typing.Dict[str, typing.Union[str, bool, int]]],
            destroyers: typing.List[typing.Dict[str, typing.Union[str, bool, int]]],
            submarines: typing.List[typing.Dict[str, typing.Union[str, bool, int]]]
    ):
        def shoot_and_check(
                board: Board,
                ships: typing.List[typing.Dict[str, typing.Union[str, bool, int]]],
                fleet_size: int, fleet_type: ChoiceItem):
            for ship in ships:
                ship['board'] = board.id
                client.post(url, data=ship, format='json')
            assert fleet_size * fleet_type == Fleet.objects.filter(
                fleet_type=ship.get('fleet_type')).count()

        client, url, board = self.create_board()
        if len(battleships) > 0:
            shoot_and_check(board, battleships, settings.BATTLESHIP_SIZE, settings.BATTLESHIP_QTY)
        if len(cruisers) > 0:
            shoot_and_check(board, cruisers, settings.CRUISER_SIZE, settings.CRUISER_QTY)
        if len(destroyers) > 0:
            shoot_and_check(board, destroyers, settings.DESTROYER_SIZE, settings.DESTROYER_QTY)
        if len(submarines) > 0:
            shoot_and_check(board, submarines, settings.SUBMARINE_SIZE, settings.SUBMARINE_QTY)
