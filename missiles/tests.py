from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from commons.tests import board
from fleets.models import Fleet
from fleets.utils import add_battleship
from missiles.models import Missile
from missiles.utils import is_dead


def test_check_dead_ship(board):
    add_battleship(board, 1, 1, vertical=False)
    Fleet.objects.update(hit=True)
    qs = Fleet.objects.all()
    assert True is is_dead(qs)


def test_check_damaged_ship(board):
    add_battleship(board, 1, 1, vertical=False)
    instance = Fleet.objects.first()
    instance.hit = True
    instance.save()
    qs = Fleet.objects.all()
    assert False is is_dead(qs)


def test_hit_battleship(board):
    add_battleship(board, 1, 1, vertical=False)
    url = reverse('api:missile-list')
    data = {
        'board': board.id,
        'x_axis': 1,
        'y_axis': 1,
    }
    client = APIClient()
    res = client.post(url, data=data, format='json')
    msg = {'message': f"Hit"}
    assert status.HTTP_201_CREATED == res.status_code
    assert msg == res.data


def test_miss_battleship(board):
    add_battleship(board, 1, 1, vertical=False)
    url = reverse('api:missile-list')
    data = {
        'board': board.id,
        'x_axis': 2,
        'y_axis': 2,
    }
    client = APIClient()
    res = client.post(url, data=data, format='json')
    msg = {'message': 'Miss'}
    assert status.HTTP_201_CREATED == res.status_code
    assert msg == res.data


def test_shoot_same_position(board):
    Missile.objects.create(board=board, x_axis=1, y_axis=1)
    url = reverse('api:missile-list')
    data = {
        'board': board.id,
        'x_axis': 1,
        'y_axis': 1,
    }
    client = APIClient()
    res = client.post(url, data=data, format='json')
    msg = f"The fields board, x_axis, y_axis must make a unique set."
    assert status.HTTP_400_BAD_REQUEST == res.status_code
    assert msg == str(res.data.get('non_field_errors')[0])


def test_sunk_battleship(board):
    add_battleship(board, 1, 1, vertical=False)
    Missile.objects.bulk_create([
        Missile(board=board, x_axis=2, y_axis=1),
        Missile(board=board, x_axis=3, y_axis=1),
        Missile(board=board, x_axis=4, y_axis=1),
    ])
    Fleet.objects.update(hit=True)
    instance = Fleet.objects.get(x_axis=1, y_axis=1)
    instance.hit = False
    instance.save()

    url = reverse('api:missile-list')
    data = {
        'board': board.id,
        'x_axis': 1,
        'y_axis': 1,
    }
    client = APIClient()
    res = client.post(url, data=data, format='json')
    msg = {'message': 'Win ! You completed the game in 4 moves. You missed 0'}
    assert status.HTTP_201_CREATED == res.status_code
    assert msg == res.data
