from django.shortcuts import get_object_or_404, redirect, render
from django.apps import apps
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest
from .models import Author
from .forms import AuthorForm, MODEL_FORMS, MODEL_TITLES_HEADERS


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

def form(request, model_name, pk=None):
    model = apps.get_model(app_label='crud', model_name=model_name)
    if not model:
        return HttpResponseBadRequest("Модель не найдена")

    form_class = MODEL_FORMS.get(model_name)
    if not form_class:
        return HttpResponseBadRequest("Форма для этой модели не найдена")

    record = get_object_or_404(model, id=pk) if pk else None

    if request.method == "POST":
        model_form = form_class(request.POST, instance=record)
        if model_form.is_valid():
            model_form.save()
            return redirect('/crud/')
    else:
        model_form = form_class(instance=record)

    return render(request, 'form.html',{
                      'form': model_form,
                      'model_title': MODEL_TITLES_HEADERS[model_name][0],
                      'model_header' : MODEL_TITLES_HEADERS[model_name][1]
    })
