from django.contrib import admin

from boards.models import Board


class BoardAdmin(admin.ModelAdmin):
    __basic_fields = ['id', 'defender', 'attacker', 'created_at', 'updated_at', 'is_done']
    list_display = __basic_fields
    list_display_links = __basic_fields
    search_fields = ['defender', 'attacker']


admin.site.register(Board, BoardAdmin)
