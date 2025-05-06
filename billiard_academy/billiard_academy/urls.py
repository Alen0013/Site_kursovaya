from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from bookings.views import index
from bookings.models import Booking
from django.shortcuts import render

def tournaments_view(request):
    bookings = Booking.objects.all()
    return render(request, 'tournaments.html', {'bookings': bookings})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bookings/', include('bookings.urls', namespace='bookings')),
    path('', index, name='index'),
    path('about-us/', TemplateView.as_view(template_name='about-us.html'), name='about_us'),
    path('tournaments/', tournaments_view, name='tournaments'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('privacy-policy/', TemplateView.as_view(template_name='privacy_policy.html'), name='privacy_policy'),
]