from django.contrib.auth.models import User
from django.db import models

from commons.utils import AbstractTimestamp


class Board(AbstractTimestamp):
    defender = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='defenders',
                                 related_query_name='defenders', null=True, blank=True)
    attacker = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='attackers',
                                 related_query_name='attackers', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.defender.username} VS {self.attacker.username}"
