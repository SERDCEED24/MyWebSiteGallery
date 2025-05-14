from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from crud.models import Artwork, Genre, Material, Technique, WorkStatus


def index(request):
    artworks = Artwork.objects.select_related('author', 'genre', 'material', 'technique', 'status').all()

    # Поиск
    query = request.GET.get('q')
    if query:
        artworks = artworks.filter(
            Q(title__icontains=query) |
            Q(genre__name__icontains=query) |
            Q(material__name__icontains=query) |
            Q(technique__name__icontains=query) |
            Q(status__name__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query) |
            Q(author__middle_name__icontains=query)
        )

    # Фильтрация
    genre = request.GET.get('genre')
    technique = request.GET.get('technique')
    material = request.GET.get('material')
    status = request.GET.get('status')

    if genre:
        artworks = artworks.filter(genre_id=genre)
    if technique:
        artworks = artworks.filter(technique_id=technique)
    if material:
        artworks = artworks.filter(material_id=material)
    if status:
        artworks = artworks.filter(status_id=status)

    # Сортировка
    sort_field = request.GET.get('sort_field')
    sort_order = request.GET.get('sort_order')
    if sort_field and sort_order:
        field_map = {
            'Название': 'title',
            'Год создания': 'creation_year',
            'Цена': 'current_price',
            'Ширина': 'width',
            'Высота': 'height',
            'Длина': 'length',
        }
        order = '' if sort_order == 'По возрастанию' else '-'
        if sort_field in field_map:
            artworks = artworks.order_by(order + field_map[sort_field])

    # Пагинация
    paginator = Paginator(artworks, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'genres': Genre.objects.all(),
        'materials': Material.objects.all(),
        'techniques': Technique.objects.all(),
        'statuses': WorkStatus.objects.all(),
        'get': request.GET
    }
    return render(request, 'base_index.html', context)

def artwork_detailed(request, pk):
    artwork = Artwork.objects.get(pk=pk)
    return render(request, 'base_artwork_detailed.html', {'artwork': artwork})