from django.urls import path
from .views import home, dashboard, subjects

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('subjects/', subjects, name='subjects'),
]