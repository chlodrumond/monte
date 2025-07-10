from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('upload/', views.upload_material, name='upload_material'),
    path('search/', views.search, name='search'),
    path('material/<int:material_id>/', views.material_detail, name='material_detail'),
    path('download/<int:material_id>/', views.download_material, name='download_material'),
    path('ranking/', views.ranking, name='ranking'),
]