from django.http import JsonResponse
from users.models import Users
from django import views


class UserLoginView(views.View):

    def get(self, request):
        return JsonResponse({"data": "你好GET请求"},status=200)


    def post(self, request):
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            data = Users.objects.filter(username=username, password=password)
            if data:
                return JsonResponse({"data":"success"}, status=200)
        return JsonResponse({"data": "error"}, status=400)


class UserRegisterView(views.View):
    def post(self, request):
        data = request
        new_user = Users.objects.create(**data)
        dict = {
            "id": new_user.id,
            "username": new_user.username
        }
        return JsonResponse(dict, status=201)