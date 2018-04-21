from django.db.models import QuerySet

from fleets.models import Fleet


def is_dead(qs: QuerySet(Fleet)) -> bool:
    tmp = True
    for point in qs:
        tmp &= point.hit
    return tmp
