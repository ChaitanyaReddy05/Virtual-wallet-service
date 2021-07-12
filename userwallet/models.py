from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    walletid = models.AutoField(primary_key=True)
    gamepoints = models.IntegerField(default=0)
    status = models.TextField(default='Active')
