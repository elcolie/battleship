from django.conf import settings

from fleets.models import Fleet


class OutOceanException(Exception):
    pass


def add_ship(board, x_axis, y_axis, ship_type, vertical: None = True):
    tmp = []
    if vertical:
        for idx_j in range(y_axis, y_axis + ship_type):
            if idx_j > settings.OCEAN_SIZE:
                raise OutOceanException(f"Out of battle zone!")
            tmp.append(Fleet(board=board, x_axis=x_axis, y_axis=idx_j, occupied=True))
        Fleet.objects.bulk_create(tmp)
    else:
        for idx_i in range(x_axis, x_axis + ship_type):
            if idx_i > settings.OCEAN_SIZE:
                raise OutOceanException(f"Out of battle zone!")
            tmp.append(Fleet(board=board, x_axis=idx_i, y_axis=y_axis, occupied=True))
        Fleet.objects.bulk_create(tmp)


def add_battleship(board, x_axis, y_axis, vertical: None = True):
    add_ship(board, x_axis, y_axis, settings.BATTLESHIP_SIZE, vertical=vertical)


def add_cruiser(board, x_axis, y_axis, vertical: None = True):
    add_ship(board, x_axis, y_axis, settings.CRUISER_SIZE, vertical=vertical)


def add_destroyer(board, x_axis, y_axis, vertical: None = True):
    add_ship(board, x_axis, y_axis, settings.DESTROYER_SIZE, vertical=vertical)


def add_submarine(board, x_axis, y_axis, vertical: None = True):
    add_ship(board, x_axis, y_axis, settings.SUBMARINE_SIZE, vertical=vertical)
