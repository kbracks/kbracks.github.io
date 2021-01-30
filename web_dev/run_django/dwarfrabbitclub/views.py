from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Camp, ItemList, PendingUser
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

# Create your views here.
class AccessForm(forms.Form):
    #usercode = forms.CharField(label="Usercode")
    campcode = forms.CharField(label="Campcode")
    def passcodeCorrect(self):
        camp = self.cleaned_data['campcode']
        #user = self.cleaned_data['usercode']
        if len(Camp.objects.filter(name = camp))==0: return False
        else: return True
        #changed to only have camp code here
        for invitee in Camp.objects.filter(name = camp).first().members.all():
            if user == invitee.code:
                return True
        return False

class CreateUserForm(forms.Form):
    full_name = forms.CharField(label="Full Name")
    #desired_username = forms.CharField(label="Desired Username")
    #desired_password = forms.CharField(label="Desired Password")
    #email_address = forms.EmailField(label="Email Address")
    #phone_number = forms.CharField(label="Phone Number")
    #personal_statement = forms.CharField(label="How did you find out about this and please include lots of detail")
#    def __dict__(self):
#        return {0: self.full_name, 1: self.desired_username, 2:self.desired_password, 3:self.email_address,4:self.phone_number,5:self.personal_statement}
    def create_pending_user(self):
        PendingUser.objects.create(name = self.cleaned_data['full_name'])#,username = self.desired_username, password = self.desired_password, email = self.email_address,phone = self.phone_number,statement = self.personal_statement)
        
        return 
    

       
def create_user(request):
    #make sure this user is pending
    # you will be contacted when your account is verified
    #pending users will not be official Users
    
    if request.method == 'POST':
        #return HttpResponse("entering form post.")
        #process the request
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.create_pending_user()
            return pending_user(request)
    else:
        return render(request, "dwarfrabbitclub/request_access.html",{'form':CreateUserForm()})

def pending_user(request):
    #a pending user cannot have access
    #you will be emailed
    num_users = len(PendingUser.objects.all())
    return render(request, "dwarfrabbitclub/access_pending.html",{'x':num_users})
        
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

#code below is not in use
#code from https://docs.djangoproject.com/en/3.1/topics/http/sessions/
def login(request):
    m = User.objects.get(username=request.POST['username'])
    if m.password == request.POST['password']:
        request.session['member_id'] = m.id
        return HttpResponse("You're logged in.")
    else:
        return HttpResponse("Your username and password didn't match.")
