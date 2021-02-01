from django.contrib import admin

# Register your models here.

from .models import Invitee, Camp, ListItem, ItemList, PendingUser, AddItem


l = [Invitee, Camp, ListItem, ItemList, PendingUser,AddItem]

for elem in l:
    admin.site.register(elem)


