from django.http import HttpResponse #a
from django.shortcuts import render
import datetime
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
    #priority = forms.IntegerField(label="Priority",min_value=1,max_value=5)

# Create your views here.
tasks = []
def root(request):
    return render(request,"madbunnyclub/root.html")
def index(request): #http request
#    if "tasks" not in request.session:
#        request.session["tasks"] = []
    return render(request,"madbunnyclub/index.html",{"tasks":tasks})#request.session["tasks"]

def names(request):
    date = datetime.datetime.now()
    
    return HttpResponse(f'Hello,Katja B. Puig {date.month} {date.day}')

def habitually(request):
    return HttpResponse("I look in the mirror habitually")

def confess(request,confession):
    return render(request,"madbunnyclub/hide.html",{"code":confession,"sum":False}) #the key should be the variable name in an html



#common pattern in here
def addTask(request): # add a check because add can request or post
    if request.method == 'POST':
        #process the request 
        form = NewTaskForm(request.POST) #contains all data that user submitted
        if form.is_valid():
            task = form.cleaned_data["task"]
            tasks.append(task) #request.session["tasks"] += [task]
            return HttpResponseRedirect(reverse('madbunnyclub:index'))
        else: return render(request, "madbunnyclub/add.html", {"form":form}) #server side validation in case client side is not up to date
    
    #the get case 
    return render(request,"madbunnyclub/add.html",{'form':NewTaskForm()}) # adde4d {'form'...} replace the <input> line in add with {{ form }} <input type="text" name="task">
