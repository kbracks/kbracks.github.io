from django.db import models
import datetime
# Create your models here.

class Date(models.Model):
    month = models.IntegerField()
    day = models.IntegerField()
    year = models.IntegerField()
    def __str__(self):
        return str(datetime.date(self.year,self.month,self.day))

class Camp(models.Model):
    location = models.CharField(max_length=64)
    start = models.ForeignKey(Date, on_delete = models.CASCADE)
    duration = models.IntegerField()
    def __str__(self):
        
        return f"{self.id}: {self.location} from {str(self.start)} for {self.duration}"
# on_delete = models.CASCADE, related_name = "___"
