from django import forms
from .models import Author


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


MODEL_TITLES_HEADERS = {
    'Author': ['автора', 'авторе']
}
MODEL_FORMS = {
    'Author': AuthorForm
}
