#i created this file
from django.urls import path
from . import views #the order of the urls matter because for instance if i have str:confession first, then it will always catch my urls

app_name = 'dwarfrabbitclub' #helps with namespace collision errors
urlpatterns = [
    path("",views.root, name='root'),
    path("entry_granted",views.entry,name='entry'),
    path("entry_granted/to_do",views.to_do,name='to_do'),
   
]
