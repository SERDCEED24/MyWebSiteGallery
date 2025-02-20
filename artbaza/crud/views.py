from django.shortcuts import get_object_or_404, redirect, render
from django.apps import apps
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest
from .models import Author, Genre, Material, Technique, WorkStatus
from .forms import MODEL_FORMS, MODEL_TITLES_HEADERS
from .constants import MODEL_TABLE_HEAD

'''
def index(request):
    authors = Author.objects.all()
    return render(request, 'index.html', {'authors': authors})
'''


def index(request, model_name):
    model = apps.get_model(app_label='crud', model_name=model_name)
    if not model:
        return HttpResponseBadRequest("Модель не найдена")
    fields = [field.name for field in model._meta.fields]
    records = model.objects.all()
    return render(request, 'index.html', {'model_name': model_name, 'fields': fields, 'records': records,
                                          'table_head': MODEL_TABLE_HEAD[model_name]})


def delete_record(request, model_name, pk):
    if request.method == "POST":
        model = apps.get_model(app_label='crud', model_name=model_name)
        if not model:
            return HttpResponseNotAllowed(['POST'], "Модель не найдена")
        record = get_object_or_404(model, pk=pk)
        record.delete()
        return redirect('/crud/')
    return HttpResponseNotAllowed(['POST'])


def form(request, model_name, pk=None):
    model = apps.get_model(app_label='crud', model_name=model_name)
    if not model:
        return HttpResponseBadRequest("Модель не найдена")

    form_class = MODEL_FORMS.get(model_name)
    if not form_class:
        return HttpResponseBadRequest("Форма для этой модели не найдена")

    record = get_object_or_404(model, id=pk) if pk else None

    if request.method == "POST":
        model_form = form_class(request.POST, request.FILES, instance=record)
        if model_form.is_valid():
            model_form.save()
            return redirect(f'/crud/{model_name}/')
    else:
        model_form = form_class(instance=record)

    return render(request, 'form.html', {
        'form': model_form,
        'model_title': MODEL_TITLES_HEADERS[model_name][0],
        'model_header': MODEL_TITLES_HEADERS[model_name][1],
        'model_name' : model_name
    })
