from django.db import models
# Yhden rivin luonti django tietokantaan.
class City(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name
# Luokka joka korjaa tablen monikkomuodon 'city':stä 'cities':ksi. 
    class Meta:
        verbose_name_plural = 'cities' 
