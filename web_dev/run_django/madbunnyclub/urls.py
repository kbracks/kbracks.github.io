#i created this file
from django.urls import path
from . import views #the order of the urls matter because for instance if i have str:confession first, then it will always catch my urls

app_name = 'madbunnyclub' #helps with namespace collision errors
urlpatterns = [
    path("",views.root, name='root'),
    path("tasks",views.index, name='index'),
    path("addTask",views.addTask,name='add'),
    
    path("names", views.names,name="names"), 
    path("name/habitually",views.habitually, name = 'habit'),
    path("<str:confession>",views.confess,name='confess'),
    
]
