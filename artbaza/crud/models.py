from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime


class Author(models.Model):
    image = models.ImageField(upload_to='authors/', blank=True, null=True)
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
        return f'{self.last_name} {self.first_name} {self.middle_name}'


class Genre(models.Model):
    genre_name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return f'{self.genre_name}'


class Material(models.Model):
    material_name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return f'{self.material_name}'


class Technique(models.Model):
    technique_name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return f'{self.technique_name}'


class WorkStatus(models.Model):
    status_name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return f'{self.status_name}'

class Artwork(models.Model):
    image = models.ImageField()
    title = models.CharField(max_length=50)
    creation_year = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(datetime.datetime.now().year)
    ])
    length = models.FloatField(blank=False, validators=[
        MinValueValidator(0)])
    width = models.FloatField(blank=False, validators=[
        MinValueValidator(0)])
    height = models.FloatField(blank=False, validators=[
        MinValueValidator(0)])
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    technique = models.ForeignKey(Technique, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    status = models.ForeignKey(WorkStatus, on_delete=models.CASCADE)
    purchase_year = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(datetime.datetime.now().year)
    ])
    purchase_price = models.FloatField(validators=[MinValueValidator(0)])
    current_price = models.FloatField(validators=[MinValueValidator(0)])
    price_without_frame = models.FloatField(validators=[MinValueValidator(0)])
    price_with_frame = models.FloatField(validators=[MinValueValidator(0)])
