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


def submarine_surrounding(board, x_axis, y_axis):
    qs = Fleet.objects.filter(
        Q(
            Q(x_axis=x_axis - 1, y_axis__in=range(y_axis - 1, y_axis + 1)) |  # left
            Q(x_axis=x_axis + 1, y_axis__in=range(y_axis - 1, y_axis + 1)) |  # right
            Q(x_axis__in=range(x_axis - 1, x_axis + 1), y_axis=y_axis - 1) |  # up
            Q(x_axis__in=range(x_axis - 1, x_axis + 1), y_axis=y_axis + 1),  # down
        ),
        occupied=True,
        board=board
    ).exists()
    if qs:
        raise NearShipException(f"Can not place submarine here. Too near!")


def generic_surrounding(board, x_axis, y_axis, ship_size, vertical: bool = True) -> bool:
    """Very simple one since it has single block"""
    if ship_size == settings.SUBMARINE_SIZE:
        submarine_surrounding(board, x_axis, y_axis)
    if vertical:
        qs = Fleet.objects.filter(
            Q(
                Q(x_axis__in=range(x_axis - 1, x_axis + 1), y_axis=y_axis - 1) |  # top
                Q(x_axis__in=range(x_axis - 1, x_axis + 1), y_axis=y_axis + ship_size) |  # bottom
                Q(x_axis=x_axis - 1, y_axis__in=range(y_axis - 1, y_axis + ship_size)) |  # left
                Q(x_axis=x_axis + 1, y_axis__in=range(y_axis - 1, y_axis + ship_size)),  # right
            ) |
            Q(
                Q(x_axis=x_axis - 1, y_axis=y_axis - 1) |  # top_left
                Q(x_axis=x_axis + 1, y_axis=y_axis - 1) |  # top_right
                Q(x_axis=x_axis - 1, y_axis=y_axis + ship_size) |  # bottom_left
                Q(x_axis=x_axis + 1, y_axis=y_axis + ship_size),  # bottom_right
            ),
            occupied=True,
            board=board
        ).exists()
    else:
        # horizontal
        qs = Fleet.objects.filter(
            Q(
                Q(x_axis__in=range(x_axis - 1, x_axis + ship_size), y_axis=y_axis - 1) |  # top
                Q(x_axis__in=range(x_axis - 1, x_axis + ship_size), y_axis=y_axis + 1) |  # bottom
                Q(x_axis=x_axis - 1, y_axis__in=range(y_axis - 1, y_axis + 1)) |  # left
                Q(x_axis=x_axis + ship_size, y_axis__in=range(y_axis - 1, y_axis + 1)),  # right
            ) |
            Q(
                Q(x_axis=x_axis - 1, y_axis=y_axis - 1) |  # top_left
                Q(x_axis=x_axis + ship_size, y_axis=y_axis - 1) |  # top_right
                Q(x_axis=x_axis - 1, y_axis=y_axis - 1) |  # bottom_left
                Q(x_axis=x_axis + ship_size, y_axis=y_axis + 1),  # bottom_right
            ),
            occupied=True,
            board=board
        ).exists()
    if qs:
        raise NearShipException(f"Too near!")


def add_battleship(board, x_axis, y_axis, vertical: bool = True):
    add_ship(board, x_axis, y_axis, settings.BATTLESHIP_SIZE, vertical=vertical)
    generic_surrounding(board, x_axis, y_axis, settings.BATTLESHIP_SIZE, vertical=vertical)


def add_cruiser(board, x_axis, y_axis, vertical: bool = True):
    add_ship(board, x_axis, y_axis, settings.CRUISER_SIZE, vertical=vertical)


def add_destroyer(board, x_axis, y_axis, vertical: bool = True):
    add_ship(board, x_axis, y_axis, settings.DESTROYER_SIZE, vertical=vertical)


def add_submarine(board, x_axis, y_axis, vertical: bool = True):
    add_ship(board, x_axis, y_axis, settings.SUBMARINE_SIZE, vertical=vertical)
    generic_surrounding(board, x_axis, y_axis, settings.SUBMARINE_SIZE, vertical=vertical)
