from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    walletid = models.AutoField(primary_key=True)

    def save(self, *args, **kwargs):
       if not wallet.objects.count():
          self.walletid = 100
       else:
          self.walletid = wallet.objects.last().walletid + 1
       super(wallet, self).save(*args, **kwargs)