from django.conf import settings
from django.db.models import Q

from fleets.models import Fleet


class OutOceanException(Exception):
    pass


class NearShipException(Exception):
    pass


def add_ship(board, x_axis, y_axis, ship_type, vertical: bool = True):
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


def submarine_surrounding(board, x_axis, y_axis, ship_size, vertical: bool = True) -> bool:
    """Very simple one since it has single block"""
    ship_size = settings.SUBMARINE_SIZE
    cross_surronding = Fleet.objects.filter(
        Q(x_axis__in=range(x_axis - 1, x_axis + ship_size), y_axis=y_axis - 1) |
        Q(x_axis__in=range(x_axis - 1, x_axis + ship_size), y_axis=y_axis + 1) |
        Q(x_axis=x_axis - 1, y_axis__in=range(y_axis - 1, y_axis + ship_size)) |
        Q(x_axis=x_axis + 1, y_axis__in=range(y_axis - 1, y_axis + ship_size)),
        occupied=True,
        board=board
    ).exists()

    qs_top_left = Fleet.objects.filter(
        x_axis=x_axis - 1,
        y_axis=y_axis - 1,
        occupied=True,
        board=board
    ).exists()
    qs_top_right = Fleet.objects.filter(
        x_axis=x_axis + 1,
        y_axis=y_axis - 1,
        occupied=True,
        board=board
    ).exists()
    qs_bottom_left = Fleet.objects.filter(
        x_axis=x_axis - 1,
        y_axis=y_axis + 1,
        occupied=True,
        board=board
    ).exists()
    qs_bottom_right = Fleet.objects.filter(
        x_axis=x_axis + 1,
        y_axis=y_axis + 1,
        occupied=True,
        board=board
    ).exists()
    # diagonal_surrounding = qs_top_left or qs_top_right or qs_bottom_left or qs_bottom_right
    diagonal_surrounding = Fleet.objects.filter(
        Q(x_axis=x_axis - 1, y_axis=y_axis - 1) |  # top_left
        Q(x_axis=x_axis + 1, y_axis=y_axis - 1) |  # top_right
        Q(x_axis=x_axis - 1, y_axis=y_axis + 1) |  # bottom_left
        Q(x_axis=x_axis + 1, y_axis=y_axis + 1),  # bottom_right
        occupied=True,
        board=board
    )
    if cross_surronding or diagonal_surrounding:
        raise NearShipException(f"Too near!")


def add_battleship(board, x_axis, y_axis, vertical: bool = True):
    add_ship(board, x_axis, y_axis, settings.BATTLESHIP_SIZE, vertical=vertical)


def add_cruiser(board, x_axis, y_axis, vertical: bool = True):
    add_ship(board, x_axis, y_axis, settings.CRUISER_SIZE, vertical=vertical)


def add_destroyer(board, x_axis, y_axis, vertical: bool = True):
    add_ship(board, x_axis, y_axis, settings.DESTROYER_SIZE, vertical=vertical)


def add_submarine(board, x_axis, y_axis, vertical: bool = True):
    add_ship(board, x_axis, y_axis, settings.SUBMARINE_SIZE, vertical=vertical)
    submarine_surrounding(board, x_axis, y_axis, settings.BATTLESHIP_SIZE, vertical=vertical)
