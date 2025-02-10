from django import forms
from .models import *


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['last_name', 'first_name', 'middle_name', 'description', 'year_of_birth', 'year_of_death']
        labels = {
            'last_name': 'Фамилия',
            'first_name': 'Имя',
            'middle_name': 'Отчество',
            'description': 'Описание',
            'year_of_birth': 'Год рождения',
            'year_of_death': 'Год смерти (не обязателен)',
        }


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['genre_name']
        labels = {
            'genre_name': 'Название жанра',
        }


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['material_name']
        labels = {
            'material_name': 'Название материала',
        }


class TechniqueForm(forms.ModelForm):
    class Meta:
        model = Technique
        fields = ['technique_name']
        labels = {
            'technique_name': 'Название техники исполнения',
        }


class WorkStatusForm(forms.ModelForm):
    class Meta:
        model = WorkStatus
        fields = ['status_name']
        labels = {
            'status_name': 'Название статуса работы',
        }


MODEL_TITLES_HEADERS = {
    'Author': ['автора', 'авторе'],
    'Genre': ['жанра', 'жанре'],
    'Material': ['материала', 'материале'],
    'Technique': ['техники исполнения', 'технике исполнения'],
    'WorkStatus': ['статуса работы', 'статусе работы'],
}
MODEL_FORMS = {
    'Author': AuthorForm,
    'Genre': GenreForm,
    'Material': MaterialForm,
    'Technique': TechniqueForm,
    'WorkStatus': WorkStatusForm,
}
