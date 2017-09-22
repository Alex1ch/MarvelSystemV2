from django.db import models
from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth.models import User


class Customer(models.Model):
    user=models.OneToOneField(to=User)

    def __str__(self):
        return self.user.username.__str__()

class Comic(models.Model):
    marvel_id=models.IntegerField(default=0)
    name = models.CharField(max_length=100, verbose_name="Имя")
    description = models.TextField(verbose_name="Описание")
    date = models.DateField(default=timezone.now,db_index=True,editable=True, verbose_name="Дата выхода")
    ean = models.CharField(max_length=30,verbose_name="EAN")
    cover_url = models.CharField(verbose_name="Обложка",max_length=200)
    characters = models.TextField(verbose_name="Персонажи")
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,verbose_name="Заказчик")



    def getShortDesc(self):
        if str(self.description).__len__()>350:
            i=350
            while str(self.description)[i]!=" ":
                i=i+1
            return str(self.description)[:i]+"..."
        else:
            return str(self.description)

    def getYear(self):
        return self.date.year.numerator;

    def __str__(self):
        return self.name+" ("+str(self.id)+")";





class ComixSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comic
        fields=('id','name','description','date','ean','cover_url','characters')

