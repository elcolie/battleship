# Generated by Django 2.0.4 on 2018-04-21 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0001_initial'),
        ('fleets', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BattleShip',
        ),
        migrations.AlterUniqueTogether(
            name='fleet',
            unique_together={('board', 'x_axis', 'y_axis', 'occupied')},
        ),
    ]
