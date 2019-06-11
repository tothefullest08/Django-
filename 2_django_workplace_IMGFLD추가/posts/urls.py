from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('create/', views.create, name="create"),
    path('', views.list, name="list"),
    path('<int:post_id>', views.detail, name="detail"),
    path('<int:post_id>/update/', views.update, name="update"),
    path('<int:post_id>/delete/', views.delete, name="delete"),
]