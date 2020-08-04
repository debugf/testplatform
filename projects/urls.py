#users/urls.py
from django.urls import path

from projects import views

urlpatterns = [
    path('', views.CreateListView.as_view()),
    path('<int:pk>', views.UpdateDeleteView.as_view()),
    path('names',views.names)
]