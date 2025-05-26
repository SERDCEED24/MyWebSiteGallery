import os

from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q

from artbaza import settings
from crud.models import Artwork, Genre, Material, Technique, WorkStatus, Author


def index(request):
    artworks = Artwork.objects.select_related('author', 'genre', 'material', 'technique', 'status').all()

    # Поиск
    query = request.GET.get('q')
    if query:
        artworks = artworks.filter(
            Q(title__icontains=query) |
            Q(genre__genre_name__icontains=query) |
            Q(material__material_name__icontains=query) |
            Q(technique__technique_name__icontains=query) |
            Q(status__status_name__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query) |
            Q(author__middle_name__icontains=query)
        )

    # Фильтрация
    genre = request.GET.get('genre')
    technique = request.GET.get('technique')
    material = request.GET.get('material')
    status = request.GET.get('status')
    author = request.GET.get('author')
    min_width = request.GET.get('min_width')
    max_width = request.GET.get('max_width')
    min_height = request.GET.get('min_height')
    max_height = request.GET.get('max_height')
    min_length = request.GET.get('min_length')
    max_length = request.GET.get('max_length')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_creation_year = request.GET.get('min_creation_year')
    max_creation_year = request.GET.get('max_creation_year')

    if genre:
        artworks = artworks.filter(genre_id=genre)
    if technique:
        artworks = artworks.filter(technique_id=technique)
    if material:
        artworks = artworks.filter(material_id=material)
    if status:
        artworks = artworks.filter(status_id=status)
    if author:
        artworks = artworks.filter(author_id=author)
    if min_width:
        artworks = artworks.filter(width__gte=min_width)
    if max_width:
        artworks = artworks.filter(width__lte=max_width)
    if min_height:
        artworks = artworks.filter(height__gte=min_height)
    if max_height:
        artworks = artworks.filter(height__lte=max_height)
    if min_length:
        artworks = artworks.filter(length__gte=min_length)
    if max_length:
        artworks = artworks.filter(length__lte=max_length)
    if min_price:
        artworks = artworks.filter(current_price__gte=min_price)
    if max_price:
        artworks = artworks.filter(current_price__lte=max_price)
    if min_creation_year:
        artworks = artworks.filter(creation_year__gte=min_creation_year)
    if max_creation_year:
        artworks = artworks.filter(creation_year__lte=max_creation_year)

    # Сортировка
    sort_field = request.GET.get('sort_field')
    sort_order = request.GET.get('sort_order')
    if sort_field and sort_order:
        field_map = {
            'Название': 'title',
            'Год создания': 'creation_year',
            'Цена': 'current_price',
            'Цена без рамы': 'price_without_frame',
            'Цена с рамой': 'price_with_frame',
            'Ширина': 'width',
            'Высота': 'height',
            'Длина': 'length',
            'Жанр': 'genre__genre_name',
            'Материал': 'material__material_name',
            'Техника': 'technique__technique_name',
            'Статус': 'status__status_name',
            'Автор': 'author__last_name'
        }
        order = '' if sort_order == 'По возрастанию' else '-'
        if sort_field in field_map:
            artworks = artworks.order_by(order + field_map[sort_field])

    # Количество элементов на странице
    per_page = request.GET.get('per_page', 6)  # По умолчанию 6
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 6
    # Ограничиваем возможные значения
    if per_page not in [3, 6, 12, 18]:
        per_page = 6
    # Пагинация
    paginator = Paginator(artworks, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'genres': Genre.objects.all(),
        'materials': Material.objects.all(),
        'techniques': Technique.objects.all(),
        'statuses': WorkStatus.objects.all(),
        'authors': Author.objects.all(),
        'get': request.GET,
        'per_page': per_page
    }
    return render(request, 'base_index.html', context)


def artwork_detailed(request, pk):
    artwork = Artwork.objects.get(pk=pk)
    author_years = ''
    if artwork.author.year_of_death:
        author_years = f'{artwork.author.year_of_birth}-{artwork.author.year_of_death}'
    else:
        author_years = f'{artwork.author.year_of_birth} г. р.'
    author_info = f'{artwork.author.last_name} {artwork.author.first_name} {artwork.author.middle_name} ({author_years})'
    artwork_numbers = {
        'height': 'Не установлена' if artwork.height == 0 else artwork.height,
        'width': 'Не установлена' if artwork.width == 0 else artwork.width,
        'length': 'Не установлена' if artwork.length == 0 else artwork.length,
        'price_without_frame': 'Не установлена' if artwork.price_without_frame == 0 else artwork.price_without_frame,
        'price_with_frame': 'Не установлена' if artwork.price_with_frame == 0 else artwork.price_with_frame,
        'current_price': 'Не установлена' if artwork.current_price == 0 else artwork.current_price,
    }
    return render(request, 'base_artwork_detailed.html',
                  {'artwork': artwork, 'author_info': author_info, 'artwork_numbers': artwork_numbers})

def download_help_user_pdf(request):
    # Путь к PDF-файлу в папке static
    pdf_path = os.path.join(settings.STATIC_ROOT, 'help', 'help_user.pdf')

    try:
        # Открываем файл и возвращаем его как ответ
        return FileResponse(
            open(pdf_path, 'rb'),
            as_attachment=True,
            filename='help_user.pdf'
        )
    except FileNotFoundError:
        return HttpResponse("Файл справки не найден", status=404)