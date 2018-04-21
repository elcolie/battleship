from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from commons.tests import board

from fleets.models import Fleet


def test_add_first_battleship_success(board):
    client = APIClient()
    url = reverse('api:fleet-list')
    data = {
        'board': board.id,
        'fleet_type': Fleet.FleetType.battleship,
        'vertical': False,
        'x_axis': 1,
        'y_axis': 1,
    }
    res = client.post(url, data=data, type='json')
    assert status.HTTP_201_CREATED == res.status_code
    assert 4 == Fleet.objects.filter(y_axis=1).count()


def test_add_first_battleship_hit_edge_top_right(board):
    client = APIClient()
    url = reverse('api:fleet-list')
    data = {
        'board': board.id,
        'fleet_type': Fleet.FleetType.battleship,
        'vertical': False,
        'x_axis': 10,
        'y_axis': 1,
    }
    res = client.post(url, data=data, type='json')
    msg = {'message': 'Out of battle zone!'}
    assert status.HTTP_400_BAD_REQUEST == res.status_code
    assert msg == res.data


def test_add_first_battleship_hit_edge_bottom_left(board):
    client = APIClient()
    url = reverse('api:fleet-list')
    data = {
        'board': board.id,
        'fleet_type': Fleet.FleetType.battleship,
        'vertical': True,
        'x_axis': 1,
        'y_axis': 10,
    }
    res = client.post(url, data=data, type='json')
    msg = {'message': 'Out of battle zone!'}
    assert status.HTTP_400_BAD_REQUEST == res.status_code
    assert msg == res.data


def test_add_first_battleship_hit_edge_bottom_right_vertical(board):
    client = APIClient()
    url = reverse('api:fleet-list')
    data = {
        'board': board.id,
        'fleet_type': Fleet.FleetType.battleship,
        'vertical': True,
        'x_axis': 10,
        'y_axis': 10,
    }
    res = client.post(url, data=data, type='json')
    msg = {'message': 'Out of battle zone!'}
    assert status.HTTP_400_BAD_REQUEST == res.status_code
    assert msg == res.data


def test_add_first_battleship_hit_edge_bottom_right_horizontal(board):
    client = APIClient()
    url = reverse('api:fleet-list')
    data = {
        'board': board.id,
        'fleet_type': Fleet.FleetType.battleship,
        'vertical': False,
        'x_axis': 10,
        'y_axis': 10,
    }
    res = client.post(url, data=data, type='json')
    msg = {'message': 'Out of battle zone!'}
    assert status.HTTP_400_BAD_REQUEST == res.status_code
    assert msg == res.data
