# bookings/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Booking
import re

def index(request):
    print("Открыта главная страница")
    return render(request, 'index.html')

def create_booking(request):
    print("Запрос получен!")
    print("Метод:", request.method)
    print("Данные:", request.POST)

    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        billiard_type = request.POST.get('billiard_type')
        phone = request.POST.get('phone')

        form_data = {
            'name': name,
            'surname': surname,
            'billiard_type': billiard_type,
            'phone': phone
        }

        print("Валидация данных:")
        print(f"Имя: {name}, Фамилия: {surname}, Тип бильярда: {billiard_type}, Телефон: {phone}")

        if not all([name, surname, billiard_type, phone]):
            messages.error(request, 'Все поля обязательны для заполнения.')
            print("Ошибка: Не все поля заполнены")
            return render(request, 'index.html', {'form_data': form_data})

        phone_pattern = r'^\+?7\s?\d{3}\s?\d{3}\s?\d{2}\s?\d{2}$|^8\s?\d{3}\s?\d{3}\s?\d{2}\s?\d{2}$'
        if not re.match(phone_pattern, phone):
            messages.error(request, 'Неверный формат номера телефона. Используйте +7 или 8 и 10 цифр (например, +7 919 354 52 82).')
            print("Ошибка: Неверный формат телефона")
            return render(request, 'index.html', {'form_data': form_data})

        valid_types = [choice[0] for choice in Booking.BILLARD_TYPES]
        if billiard_type not in valid_types:
            messages.error(request, 'Неверный тип бильярда.')
            print("Ошибка: Неверный тип бильярда")
            return render(request, 'index.html', {'form_data': form_data})

        try:
            print("Попытка сохранить бронирование...")
            phone_cleaned = phone.replace(" ", "")
            booking = Booking.objects.create(
                name=name.strip(),
                surname=surname.strip(),
                billiard_type=billiard_type,
                phone=phone_cleaned
            )
            print("Бронирование успешно сохранено:", booking)
            messages.success(request, 'Бронирование успешно создано!')
            # Сохраняем ID бронирования в сессии
            request.session['booking_id'] = booking.id
            response = redirect('bookings:booking_success')
            print("Перенаправление на booking_success:", response)
            return response
        except Exception as e:
            print(f"Ошибка при сохранении: {str(e)}")
            messages.error(request, f'Ошибка при создании бронирования: {str(e)}')
            return render(request, 'index.html', {'form_data': form_data})

    print("Перенаправление на главную страницу (не POST-запрос)")
    response = redirect('index')
    print("Перенаправление на index:", response)
    return response

def booking_success(request):
    print("Открыта страница booking_success")
    # Извлекаем ID бронирования из сессии
    booking_id = request.session.get('booking_id')
    booking = None
    if booking_id:
        try:
            booking = Booking.objects.get(id=booking_id)
            # Удаляем ID из сессии после использования
            del request.session['booking_id']
        except Booking.DoesNotExist:
            print("Бронирование не найдено по ID:", booking_id)
    else:
        print("ID бронирования не найден в сессии")
    return render(request, 'bookings/booking_success.html', {'booking': booking})

def booking_list(request):
    print("Открыта страница booking_list")
    bookings = Booking.objects.all()
    print("Найденные бронирования:", list(bookings))
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})

@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        billiard_type = request.POST.get('billiard_type')
        phone = request.POST.get('phone')

        if not all([name, surname, billiard_type, phone]):
            messages.error(request, 'Все поля обязательны для заполнения.')
            return redirect('tournaments')

        phone_pattern = r'^\+?7\s?\d{3}\s?\d{3}\s?\d{2}\s?\d{2}$|^8\s?\d{3}\s?\d{3}\s?\d{2}\s?\d{2}$'
        if not re.match(phone_pattern, phone):
            messages.error(request, 'Неверный формат номера телефона.')
            return redirect('tournaments')

        valid_types = [choice[0] for choice in Booking.BILLARD_TYPES]
        if billiard_type not in valid_types:
            messages.error(request, 'Неверный тип бильярда.')
            return redirect('tournaments')

        try:
            phone_cleaned = phone.replace(" ", "")
            booking.name = name.strip()
            booking.surname = surname.strip()
            booking.billiard_type = billiard_type
            booking.phone = phone_cleaned
            booking.save()
            messages.success(request, 'Бронирование успешно обновлено!')
        except Exception as e:
            messages.error(request, f'Ошибка при обновлении бронирования: {str(e)}')
        return redirect('tournaments')
    return redirect('tournaments')

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        try:
            booking.delete()
            messages.success(request, 'Бронирование успешно удалено!')
        except Exception as e:
            messages.error(request, f'Ошибка при удалении бронирования: {str(e)}')
    return redirect('tournaments')