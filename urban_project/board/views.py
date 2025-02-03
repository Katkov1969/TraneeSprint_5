from django.shortcuts import render, redirect
from board.models import Advertisement
from board.forms import AdvertisementForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

def logout_view(request):
    logout(request)
    return redirect('home')

from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login, authenticate

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/board')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def advertisement_list(request):
    advertisements = Advertisement.objects.all()
    return render(request, 'board/advertisement_list.html', {'advertisements': advertisements})

def advertisement_detail(request, pk):
    advertisement = Advertisement.objects.get(pk=pk)
    return render(request, 'board/advertisement_detail.html', {'advertisement': advertisement})

@login_required
def add_advertisement(request):
    if request.method == "POST":
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.author = request.user
            advertisement.save()
            return redirect('board:advertisement_list')
    else:
        form = AdvertisementForm()
    return render(request, 'board/add_advertisement.html', {'form': form})


@login_required
def edit_advertisement(request, pk: int):
    """
    Представление для редактирования существующего объявления.
    Загружает данные объявления в форму, обрабатывает изменения и сохраняет их.

    :param request: HTTP запрос от клиента.
    :param pk: Первичный ключ (ID) объявления для редактирования.
    :return: HTTP ответ с шаблоном редактирования или перенаправление на список объявлений.
    """
    # Получаем объявление по ID или возвращаем 404
    advertisement = get_object_or_404(Advertisement, pk=pk)

    # Проверяем, что текущий пользователь является автором объявления
    if advertisement.author != request.user:
        return HttpResponseForbidden("Вы не можете редактировать это объявление.")

    # Если метод POST, обрабатываем отправку формы
    if request.method == "POST":
        # Связываем форму с существующим объектом (instance=advertisement)
        form = AdvertisementForm(request.POST, instance=advertisement)
        if form.is_valid():
            # Сохраняем изменения
            form.save()
            # Перенаправляем на страницу списка объявлений после успешного сохранения
            return redirect('board:advertisement_list')
    else:
        # Если метод GET, отображаем форму с предзаполненными данными
        form = AdvertisementForm(instance=advertisement)

    # Рендерим шаблон с формой редактирования
    return render(request, 'board/edit_advertisement.html', {'form': form, 'advertisement': advertisement})