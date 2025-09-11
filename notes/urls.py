from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/edit/", views.update, name="update"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("tags/", views.tag_list, name="tag_list"),             # <= aqui
    path("tags/<int:tag_id>/", views.tag_detail, name="tag_detail"),
]
