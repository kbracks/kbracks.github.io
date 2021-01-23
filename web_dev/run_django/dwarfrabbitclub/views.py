from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.
class AccessForm(forms.Form):
    usercode = forms.CharField(label="Usercode")
    campcode = forms.CharField(label="Campcode")
    def passcodeCorrect(self):
        return self.cleaned_data['campcode'] == 'camp0' and self.cleaned_data['usercode'] == 'mad_bunny_lover'
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
    return render(request,"dwarfrabbitclub/to_do.html")
