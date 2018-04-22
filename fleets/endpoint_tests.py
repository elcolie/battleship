from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from commons.conftest import board, battleship, cruiser1, cruiser2, destroyer1, destroyer2, destroyer3, submarine1, \
    submarine2, submarine3, submarine4

from fleets.models import Fleet
from fleets.utils import add_battleship
from django.conf import settings


def test_add_first_battleship_success(board, battleship):
    client = APIClient()
    url = reverse('api:fleet-list')
    res = client.post(url, data=battleship, type='json')
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


def test_add_cruiser(board, cruiser1):
    client = APIClient()
    url = reverse('api:fleet-list')
    res = client.post(url, data=cruiser1, type='json')
    assert status.HTTP_201_CREATED == res.status_code
    assert 3 == Fleet.objects.filter(y_axis=4).count()


def test_add_near_cruiser_battleship(board):
    add_battleship(board, 5, 5, vertical=False)
    client = APIClient()
    url = reverse('api:fleet-list')
    data = {
        'board': board.id,
        'fleet_type': Fleet.FleetType.cruiser,
        'vertical': False,
        'x_axis': 4,
        'y_axis': 4,
    }
    res = client.post(url, data=data, type='json')
    msg = {'message': 'Too near!'}
    assert status.HTTP_400_BAD_REQUEST == res.status_code
    assert msg == res.data
    assert 4 == Fleet.objects.filter(y_axis=5).count()


def test_add_curiser_near_battleship_tail(board, battleship):
    client = APIClient()
    url = reverse('api:fleet-list')
    res1 = client.post(url, data=battleship, format='json')
    assert status.HTTP_201_CREATED == res1.status_code

    # (1,1), (1,2), (1,3), (1,4)
    #                           (5, 2) (6,2) (7,2)
    cruiser = {
        'board': board.id,
        'fleet_type': Fleet.FleetType.cruiser,
        'vertical': False,
        'x_axis': 5,
        'y_axis': 2,
    }
    res = client.post(url, data=cruiser, format='json')
    msg = {'message': 'Too near!'}
    assert status.HTTP_400_BAD_REQUEST == res.status_code
    assert msg == res.data


def test_add_two_battleship_api(board, battleship):
    client = APIClient()
    url = reverse('api:fleet-list')
    res1 = client.post(url, data=battleship, type='json')
    assert status.HTTP_201_CREATED == res1.status_code

    data = {
        'board': board.id,
        'fleet_type': Fleet.FleetType.battleship,
        'vertical': False,
        'x_axis': 5,
        'y_axis': 5,
    }
    res2 = client.post(url, data=data, type='json')
    msg = f"tiras VS sarit has battleship over quota"
    assert status.HTTP_400_BAD_REQUEST == res2.status_code
    assert msg == str(res2.data.get('board')[0])


def test_add_curiser_over_quota(board, cruiser1, cruiser2):
    client = APIClient()
    url = reverse('api:fleet-list')
    res = client.post(url, data=cruiser1, format='json')
    res = client.post(url, data=cruiser2, format='json')
    cruiser3 = {
        'board': board.id,
        'fleet_type': Fleet.FleetType.cruiser,
        'vertical': False,
        'x_axis': 7,
        'y_axis': 9,
    }
    res = client.post(url, data=cruiser3, format='json')
    msg = f'tiras VS sarit has cruiser over quota'
    assert status.HTTP_400_BAD_REQUEST == res.status_code
    assert msg == str(res.data.get('board')[0])
    assert settings.CRUISER_SIZE * settings.CRUISER_QTY == Fleet.objects.filter(
        fleet_type=Fleet.FleetType.cruiser).count()


def test_add_destroyer_over_quota(board, destroyer1, destroyer2, destroyer3):
    client = APIClient()
    url = reverse('api:fleet-list')
    res1 = client.post(url, data=destroyer1, format='json')
    res2 = client.post(url, data=destroyer2, format='json')
    res3 = client.post(url, data=destroyer3, format='json')
    destroyer4 = {
        'board': board.id,
        'fleet_type': Fleet.FleetType.destroyer,
        'vertical': False,
        'x_axis': 7,
        'y_axis': 9,
    }
    res4 = client.post(url, data=destroyer4, format='json')
    msg = f'tiras VS sarit has destroyer over quota'
    assert status.HTTP_400_BAD_REQUEST == res4.status_code
    assert msg == str(res4.data.get('board')[0])
    assert settings.DESTROYER_SIZE * settings.DESTROYER_QTY == Fleet.objects.filter(
        fleet_type=Fleet.FleetType.destroyer).count()


def test_add_submarine_over_quota(board, submarine1, submarine2, submarine3, submarine4):
    client = APIClient()
    url = reverse('api:fleet-list')
    res1 = client.post(url, data=submarine1, format='json')
    res2 = client.post(url, data=submarine2, format='json')
    res3 = client.post(url, data=submarine3, format='json')
    res4 = client.post(url, data=submarine4, format='json')
    submarine5 = {
        'board': board.id,
        'fleet_type': Fleet.FleetType.submarine,
        'vertical': False,
        'x_axis': 7,
        'y_axis': 9,
    }
    res = client.post(url, data=submarine5, format='json')
    msg = f'tiras VS sarit has submarine over quota'
    assert status.HTTP_400_BAD_REQUEST == res.status_code
    assert msg == str(res.data.get('board')[0])


def test_place_full_fleets(board, battleship, cruiser1, cruiser2, destroyer1, destroyer2, destroyer3, submarine1,
                           submarine2, submarine3, submarine4):
    """https://docs.google.com/spreadsheets/d/14tlykHCmp27zXwoZj2ZhvbvmbxwOVi3JGxb97HDm3gU/edit?usp=sharing"""
    client = APIClient()
    url = reverse('api:fleet-list')
    res = client.post(url, data=battleship, format='json')

    res = client.post(url, data=cruiser1, format='json')
    res = client.post(url, data=cruiser2, format='json')

    res = client.post(url, data=destroyer1, format='json')
    res = client.post(url, data=destroyer2, format='json')
    res = client.post(url, data=destroyer3, format='json')

    res = client.post(url, data=submarine1, format='json')
    res = client.post(url, data=submarine2, format='json')
    res = client.post(url, data=submarine3, format='json')
    res = client.post(url, data=submarine4, format='json')

    assert settings.BATTLESHIP_SIZE * settings.BATTLESHIP_QTY == Fleet.objects.filter(
        fleet_type=Fleet.FleetType.battleship).count()
    assert settings.CRUISER_SIZE * settings.CRUISER_QTY == Fleet.objects.filter(
        fleet_type=Fleet.FleetType.cruiser).count()
    assert settings.DESTROYER_SIZE * settings.DESTROYER_QTY == Fleet.objects.filter(
        fleet_type=Fleet.FleetType.destroyer).count()
    assert settings.SUBMARINE_SIZE * settings.SUBMARINE_QTY == Fleet.objects.filter(
        fleet_type=Fleet.FleetType.submarine).count()
