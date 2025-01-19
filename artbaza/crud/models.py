from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime


class Author(models.Model):
    first_name = models.CharField(max_length=20, blank=False)
    middle_name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=20, blank=False)
    description = models.TextField()
    year_of_birth = models.IntegerField(blank=False, validators=[
        MinValueValidator(0),
        MaxValueValidator(datetime.datetime.now().year)
    ])
    year_of_death = models.IntegerField(null=True, blank=True, validators=[
        MinValueValidator(0),
        MaxValueValidator(datetime.datetime.now().year)
    ])

    def __str__(self):
        return f'{self.first_name} {self.middle_name} {self.last_name} {self.description} {self.year_of_birth} {self.year_of_death}'
