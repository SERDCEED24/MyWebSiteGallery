from django.shortcuts import get_object_or_404, redirect, render
from django.apps import apps
from django.http import HttpResponseNotAllowed
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
