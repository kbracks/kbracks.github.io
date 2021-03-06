from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Camp, ItemList, PendingUser, UserSession
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session



from django.contrib.auth.signals import user_logged_in



def user_logged_in_handler(sender, request, user, **kwargs):
    UserSession.objects.get_or_create(
        user = user,
        session_id = request.session.session_key
    )
    

user_logged_in.connect(user_logged_in_handler)

#def delete_user_sessions(user): #not used code
#    user_sessions = UserSession.objects.filter(user = user)
#    for user_session in user_sessions:
#        user_session.session.delete()



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
    desired_username = forms.CharField(label="Desired Username")
    desired_password = forms.CharField(label="Desired Password")
    email_address = forms.EmailField(label="Email Address")
    phone_number = forms.CharField(label="Phone Number")
    personal_statement = forms.CharField(label="How did you find out about this and please include lots of detail")
#    def __dict__(self):
#        return {0: self.full_name, 1: self.desired_username, 2:self.desired_password, 3:self.email_address,4:self.phone_number,5:self.personal_statement}
    def create_pending_user(self):
        c_name = self.cleaned_data['full_name']
        c_username = self.cleaned_data['desired_username']
        c_password = self.cleaned_data['desired_password']
        c_email = self.cleaned_data['email_address']
        c_phone = self.cleaned_data['phone_number']
        c_statement = self.cleaned_data['personal_statement']
        PendingUser.objects.create(name = c_name,username = c_username, password = c_password, email = c_email,phone = c_phone,statement = c_statement)
        
        return 
    
class AcceptPending(forms.Form):
    user = forms.IntegerField(label = 'Pending User ID to Accept')
    
       
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
    #if not request.user.is_authenticated: return render(request,'registration/login.html')
    if request.user.has_perm('dwarfrabbitclub.can_modify'):
        destination = "dwarfrabbitclub/entry_admin.html"
    else: destination = "dwarfrabbitclub/entry.html"
    return render(request,destination)

def modify_pending(request):
    if request.method == 'POST':
        form = AcceptPending(request.POST)
        if form.is_valid():
            i_d = form.cleaned_data['user']
            p_u = PendingUser.objects.all().get(id=i_d)
            new_user = User(username = p_u.username)
            new_user.set_password(p_u.password)
            new_user.save()
            PendingUser.objects.filter(id=p_u.id).delete()
    return render(request, "dwarfrabbitclub/modify_pending.html",{'pending_users':PendingUser.objects.all(),'form':AcceptPending()})

def to_do(request):
#in admin when i create a new item it is not added to the item list automatically
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
