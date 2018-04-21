import pytest
from django.contrib.auth.models import User
from model_mommy import mommy

from boards.models import Board


@pytest.fixture
def board(db):
    mbx = mommy.make(User, username='sarit')
    lullalab = mommy.make(User, username='trash')
    return mommy.make(Board, defender=lullalab, attacker=mbx, is_done=False)
