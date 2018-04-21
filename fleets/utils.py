from django.conf import settings

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
    # lower
    qs1 = Fleet.objects.filter(
        x_axis__in=range(x_axis - 1, x_axis + ship_size),
        y_axis=y_axis - 1,
        occupied=True,
        board=board
    ).exists()
    # upper
    qs2 = Fleet.objects.filter(
        x_axis__in=range(x_axis - 1, x_axis + ship_size),
        y_axis=y_axis + 1,
        occupied=True,
        board=board
    ).exists()
    # left
    qs3 = Fleet.objects.filter(
        x_axis=x_axis - 1,
        y_axis__in=range(y_axis - 1, y_axis + ship_size),
        occupied=True,
        board=board
    ).exists()
    # right
    qs4 = Fleet.objects.filter(
        x_axis=x_axis + 1,
        y_axis__in=range(y_axis - 1, y_axis + ship_size),
        occupied=True,
        board=board
    ).exists()
    cross_surronding = qs1 or qs2 or qs3 or qs4

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
    diagonal_surrounding = qs_top_left or qs_top_right or qs_bottom_left or qs_bottom_right
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
