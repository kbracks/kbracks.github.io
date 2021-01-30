from django.db import models
import datetime
# Create your models here.

class Date(models.Model):
    month = models.IntegerField()
    day = models.IntegerField()
    year = models.IntegerField()
    def __str__(self):
        return str(datetime.date(self.year,self.month,self.day))


class Invitee(models.Model):
    code = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.code}: {self.name}"


class Camp(models.Model):
    
    #start = models.ForeignKey(Date, on_delete = models.CASCADE)
    name = models.CharField(max_length=64)
    members = models.ManyToManyField(Invitee, through="GrantAccess")
    def __str__(self):
        
        return self.name + 'camp'
# on_delete = models.CASCADE, related_name = "___"

class GrantAccess(models.Model):
    invitee = models.ForeignKey(Invitee, on_delete = models.CASCADE)
    camp = models.ForeignKey(Camp, on_delete = models.CASCADE)
    

class ListItem(models.Model):
    name = models.CharField(max_length=64)
    quantity = models.IntegerField()
    def __str__(self):
        return self.name

class ItemList(models.Model):
    items = models.ManyToManyField(ListItem,through='AddItem')
    def __str__(self):
        return f'List of length {len(self.items.all())}'


class AddItem(models.Model):
    item = models.ForeignKey(ListItem,on_delete = models.CASCADE)
    lst = models.ForeignKey(ItemList,on_delete = models.CASCADE)
    
class PendingUser(models.Model):
    name = models.CharField(max_length=64)
#    username = models.CharField(max_length=64)
#    password = models.CharField(max_length=64)
#    email = models.EmailField(max_length=64)
#    phone = models.CharField(max_length=64)
#    statement = models.CharField(max_length=128)
#    
