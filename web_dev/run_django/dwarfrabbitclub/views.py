from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Camp, ItemList
# Create your views here.
class AccessForm(forms.Form):
    usercode = forms.CharField(label="Usercode")
    campcode = forms.CharField(label="Campcode")
    def passcodeCorrect(self):
        camp = self.cleaned_data['campcode']
        user = self.cleaned_data['usercode']
        if len(Camp.objects.filter(name = camp))==0: return False
        for invitee in Camp.objects.filter(name = camp).first().members.all():
            if user == invitee.code:
                return True
        return False

            
            
        
def root(request):
    if request.method == 'POST':
        #process the request 
        form = AccessForm(request.POST) #contains all data that user submitted
        if form.is_valid() and form.passcodeCorrect() :
            return HttpResponseRedirect(reverse('dwarfrabbitclub:entry'))
        else: return render(request, "dwarfrabbitclub/root.html", {"form":form}) #server side validation in case client side is not up to date
    
    #the get case 
    
    return render(request,"dwarfrabbitclub/root.html",{'form':AccessForm()})


def entry(request):
    return render(request,"dwarfrabbitclub/entry.html")


def to_do(request):
    return render(request,"dwarfrabbitclub/to_do.html", {"item_list":ItemList.objects.all().first().items.all()})
