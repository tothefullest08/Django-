from django.urls import path
from . import views
from rest_framework_swagger.views import get_swagger_view

urlpatterns = [
    path('musics/', views.music_list),
    path('musics/<int:music_id>/', views.music_detail),
    path('docs/', get_swagger_view(title='API Docs')),
    path('artists/', views.artist_list),
    path('artists/<int:artist_id>/', views.artist_detail),
    path('musics/<int:music_id>/comments/', views.comment_create),
    path('musics/<int:music_id>/comments/<int:comment_id>/', views.comment_update_and_delete),

]