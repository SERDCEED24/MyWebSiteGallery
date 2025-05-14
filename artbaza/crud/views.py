from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from django.apps import apps
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest
import json
from .models import Author, Genre, Material, Technique, WorkStatus
from .forms import MODEL_FORMS, MODEL_TITLES_HEADERS
from .constants import MODEL_TABLE_HEAD
from .models import Artwork
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
'''
def index(request):
    authors = Author.objects.all()
    return render(request, 'index.html', {'authors': authors})
'''


@login_required
def index(request, model_name):
    model = apps.get_model(app_label='crud', model_name=model_name)
    if not model:
        return HttpResponseBadRequest("Модель не найдена")
    if model_name == 'Artwork':
        fields = ['id', 'image', 'title', 'creation_year', 'author', 'status', 'current_price']
    else:
        fields = [field.name for field in model._meta.fields]

    query = request.GET.get("q", "").strip()

    records = model.objects.all()
    if query:
        match model_name:
            case 'Author':
                records = records.filter(Q(last_name__icontains=query) | Q(id__icontains=str(query)))
            case 'Genre':
                records = records.filter(Q(genre_name__icontains=query) | Q(id__icontains=str(query)))
            case 'Material':
                records = records.filter(Q(material_name__icontains=query) | Q(id__icontains=str(query)))
            case 'Technique':
                records = records.filter(Q(technique_name__icontains=query) | Q(id__icontains=str(query)))
            case 'WorkStatus':
                records = records.filter(Q(status_name__icontains=query) | Q(id__icontains=str(query)))
            case 'Artwork':
                records = records.filter(Q(title__icontains=query) | Q(id__icontains=str(query)))

    sort_field = request.GET.get('sort', '')
    direction = request.GET.get('direction', 'asc')

    if sort_field and sort_field in fields:
        if direction == 'desc':
            records = records.order_by(f'-{sort_field}')
        else:
            records = records.order_by(sort_field)

    field_label = []
    for i in range(len(fields)):
        field_label.append([fields[i], MODEL_TABLE_HEAD.get(model_name)[i]])

    return render(request, 'index.html', {
            'model_name': model_name,
            'fields': fields,
            'records': records,
            'sort_field': sort_field,
            'table_head': MODEL_TABLE_HEAD.get(model_name),
            'field_label': field_label,
            'direction': direction,
    })

@login_required
def delete_record(request, model_name, pk):
    if request.method == "POST":
        model = apps.get_model(app_label='crud', model_name=model_name)
        if not model:
            return JsonResponse({"error": "Модель не найдена"}, status=400)

        record = get_object_or_404(model, pk=pk)
        record.delete()
        return JsonResponse({"success": True, "record_id": pk})

    return JsonResponse({"error": "Метод не разрешён"}, status=405)

def delete_treenode(request, model_name, pk):
    try:
        model_map = {
            'Author': Author,
            'Genre': Genre,
            'Material': Material,
            'Technique': Technique,
            'WorkStatus': WorkStatus,
            'Artwork': Artwork
        }

        model = model_map.get(model_name)
        if not model:
            return JsonResponse({"success": False, "error": "Модель не найдена"}, status=400)

        obj = model.objects.get(id=pk)
        obj.delete()

        return JsonResponse({"success": True})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)

@login_required
def form(request, model_name, pk=None):
    model = apps.get_model(app_label='crud', model_name=model_name)
    if not model:
        return HttpResponseBadRequest("Модель не найдена")

    form_class = MODEL_FORMS.get(model_name)
    if not form_class:
        return HttpResponseBadRequest("Форма для этой модели не найдена")

    record = get_object_or_404(model, id=pk) if pk else None

    if request.method == "GET":
        referer = request.META.get('HTTP_REFERER', None)
        if referer:
            request.session['referer'] = referer

    referer = request.session.get('referer', None)
    if not referer:
        return redirect(f'/crud/{model_name}/')

    if request.method == "POST":
        model_form = form_class(request.POST, request.FILES, instance=record)
        if model_form.is_valid():
            model_form.save()
            return redirect(referer)
    else:
        model_form = form_class(instance=record)

    return render(request, 'form.html', {
        'form': model_form,
        'model_title': MODEL_TITLES_HEADERS[model_name][0],
        'model_header': MODEL_TITLES_HEADERS[model_name][1],
        'model_name' : model_name
    })

@login_required
def artwork_detailed(request, pk):
    artwork = Artwork.objects.get(pk=pk)
    return render(request, 'artwork_detailed.html', {'artwork': artwork})

def register(request):
    if request.method == 'POST':
        form_ = UserCreationForm(request.POST)
        if form_.is_valid():
            user = form_.save()
            login(request, user)
            return redirect('/crud/Artwork/')
    else:
        form_ = UserCreationForm()
    return render(request, 'register.html', {'form': form_})

def tree_view(request):
    context = {
        'authors': Author.objects.all(),
        'genres': Genre.objects.all(),
        'materials': Material.objects.all(),
        'techniques': Technique.objects.all(),
        'statuses': WorkStatus.objects.all(),
        'artworks': Artwork.objects.all()
    }
    return render(request, 'tree_view.html', context)


@login_required
def delete_multiple(request, model_name):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            ids = data.get("ids", [])
            if not ids:
                return JsonResponse({"success": False, "error": "Нет выбранных записей"})
            model = apps.get_model(app_label='crud', model_name=model_name)
            if not model:
                return HttpResponseBadRequest("Модель не найдена")
            model.objects.filter(id__in=ids).delete()
            return JsonResponse({"success": True})
        except (ObjectDoesNotExist, json.JSONDecodeError) as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Неверный метод запроса"})