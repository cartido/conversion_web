from django.db import models

# Create your models here.
class Matter(models.Model):
    name = models.CharField(max_length=100)
    density = models.FloatField(verbose_name="kg/m3")