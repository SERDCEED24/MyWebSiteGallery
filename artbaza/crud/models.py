from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime


class Author(models.Model):
    last_name = models.CharField(max_length=20, blank=False)
    first_name = models.CharField(max_length=20, blank=False)
    middle_name = models.CharField(max_length=20, blank=False)
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
        return f'{self.last_name} {self.first_name} {self.middle_name} {self.description} {self.year_of_birth} {self.year_of_death}'


class Genre(models.Model):
    genre_name = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return f'{self.genre_name}'


class Material(models.Model):
    material_name = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return f'{self.material_name}'


class Technique(models.Model):
    technique_name = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return f'{self.technique_name}'


class WorkStatus(models.Model):
    status_name = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return f'{self.status_name}'
