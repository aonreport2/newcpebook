from django.db import models
from django.contrib.auth.models import AbstractUser, User


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    edu = models.CharField(max_length=2)
    std = models.CharField(max_length=20)
    cpenumber = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)
    count = models.CharField(max_length=2)

    def __str__(self):
        return self.user.username

class OderCommand(models.Model):
    idcpesend = models.IntegerField(max_length=11)
    status = models.BooleanField(default=False)
    idcpeto = models.IntegerField(max_length=11)
    date = models.DateTimeField(auto_now_add=True)

    class Meta :
        db_table = 'odercommand'
        ordering =('date',)
        verbose_name = 'รายการที่'
        verbose_name_plural = 'รายการ'

        def __str__(self):
            return self.user.username


class OderItem(models.Model):
    oder = models.ForeignKey(OderCommand,on_delete=models.CASCADE)

    class Meta:
        db_table = 'oderitem'
        verbose_name = 'รายการที่'
        verbose_name_plural = 'รายการ'

    def __str__(self):
        return self.oder





