from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Player, Match

admin.site.register(Player)
admin.site.register(Match)
