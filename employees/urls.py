# employees/urls.py
from django.urls import path

from employees import views
urlpatterns = [
    # as_view()：自动查找views.EmployeesListCreateView里面相匹配的试图函数
    path('employee/', views.EmployeesListCreateView.as_view()),
    # <int:pk>：接收int类型的路径参数
    path('employee/<int:pk>/', views.EmployeesRetrieveUpdateDestroyView.as_view()),
    path('employee/names/', views.EmployeesRetrieveUpdateDestroyView.as_view(), name="names")
]