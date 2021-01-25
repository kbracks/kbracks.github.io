from django.contrib import admin

# Register your models here.

from .models import Invitee, Camp, ListItem, ItemList

l = [Invitee, Camp, ListItem, ItemList]

for elem in l:
    admin.site.register(elem)
