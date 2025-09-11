from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/edit/', views.update, name='update'), 
    path('<int:pk>/delete/', views.delete, name='delete'),
]