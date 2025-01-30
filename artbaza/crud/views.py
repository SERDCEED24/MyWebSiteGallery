from django.shortcuts import get_object_or_404, redirect, render
from django.apps import apps
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest
from .models import Author

def index(request):
    authors = Author.objects.all()
    return render(request, 'index.html', {'authors': authors})


def delete_record(request, model_name, pk):
    if request.method == "POST":
        model = apps.get_model(app_label='crud', model_name=model_name)
        if not model:
            return HttpResponseNotAllowed(['POST'], "Модель не найдена")
        record = get_object_or_404(model, pk=pk)
        record.delete()
        return redirect('/crud/')
    return HttpResponseNotAllowed(['POST'])

def add_record(request, model_name):
    if request.method == "POST":
        model = apps.get_model(app_label='crud', model_name=model_name)
        if not model:
            return HttpResponseNotAllowed(['POST'], "Модель не найдена")
        fields = {}
        for field in model._meta.fields:
            if field.name in request.POST:
                value = request.POST.get(field.name)
                # Обрабатываем пустую строку для числовых и других nullable полей
                if value == '' and (field.null or field.blank):
                    value = None
                fields[field.name] = value
        try:
            record = model.objects.create(**fields)
        except Exception as e:
            return HttpResponseBadRequest(f"Ошибка: {str(e)}")
        return redirect('/crud/')
    return HttpResponseNotAllowed(['POST'])

def form(request, model_name, pk):
    if request.method == "GET":
        model = apps.get_model(app_label='crud', model_name=model_name)
        if not model:
            return HttpResponseNotAllowed(['GET'], "Модель не найдена")
        if pk != -1:
            record = get_object_or_404(model, pk=pk)
        else:
            pass
    return  render(request, 'form.html')