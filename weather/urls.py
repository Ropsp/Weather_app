from django.urls import path
from . import views
# Määrittää osoitteen.
urlpatterns = [
    path('', views.index, name='main'),
    path('delete/<city_name>/', views.delete_city, name='delete_city')
]