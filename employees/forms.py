from django import forms

from employees.models import Employees

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employees
        fields = '__all__'
        exclude = ['is_delete']
