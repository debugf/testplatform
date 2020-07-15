from django.http import JsonResponse, HttpResponse
from users.models import Users
from django import views


class UserLoginView(views.View):

    def post(self, request):
        json_data = request.body.decode('utf-8')
        python_data = eval(json_data)
        username = python_data.get('username')
        password = python_data.get('password')
        data = Users.objects.filter(username=username, password=password).first()
        if data:
            dict = {"id": data.id, "username": data.username}
            return JsonResponse(dict, status=200)
        return JsonResponse({"data": "无效用户名或密码"}, status=400)


class UserRegisterView(views.View):

    def post(self, request):
        json_data = request.body.decode('utf-8')
        python_data = eval(json_data)
        if python_data.get("username") and python_data.get("password") and python_data.get("email"):
            try:
                new_user = Users.objects.create(**python_data)
                dict = {"id": new_user.id, "username": new_user.username}
                return JsonResponse(dict, status=201)
            except Exception as e:
                return JsonResponse({"data_error": str(e)}, status=400)
        return JsonResponse({"data": "所有字段为必填项"}, status=400)
