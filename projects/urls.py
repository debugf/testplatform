#users/urls.py
from django.urls import path

from projects import views

urlpatterns = [
    path('', views.CreateListView.as_view()),
    # path('register', views.RegisterView.as_view()),
    # path('demo', views.demo)
]