# users/views.py
from django.http import JsonResponse
from django.views import View

from users.forms import RegisterForm
from users.generate_token import generate_jwt_token
from users.models import Users
from utils.jwt_permission_required import auth_permission_required
from utils.common import result


class LoginView(View):
    def post(self, request):
        result["message"] = "登录失败"
        result["success"] = False
        result["details"] = None
        json_data = request.body.decode('utf-8')
        if json_data:
            python_data = eval(json_data)
            username = python_data.get('username')
            password = python_data.get('password')
            data = Users.objects.filter(username=username, password=password).values("id", "username").first()
            if data:
                token = generate_jwt_token(username)
                result["message"] = "登录成功"
                result["success"] = True
                result["details"] = {"id": data["id"], "username": data["username"],"token": token}
                return JsonResponse(result, status=200)
            result["details"] = "用户名或密码错误"
            return JsonResponse(result, status=400)
        return JsonResponse(result, status=500)


class RegisterView(View):
    def post(self, request):
        result["message"] = "注册失败"
        result["success"] = False
        result["details"] = None
        json_data = request.body.decode('utf-8')
        if json_data:
            python_data = eval(json_data)
            data = RegisterForm(python_data)
            if data.is_valid():
                data.cleaned_data.pop("r_password")
                Users.objects.create(**data.cleaned_data)
                data.cleaned_data.pop("password")
                result["message"] = "注册成功"
                result["success"] = True
                result["details"] = data.cleaned_data
                return JsonResponse(result, status=200)
            else:
                result["details"] = data.errors
                return JsonResponse(result, status=400)
        return JsonResponse(result, status=500)

@auth_permission_required("func")
def demo(request):
    if request.method == 'GET':
        return JsonResponse({"state": 1, "message": "token有效"})
    else:
        return JsonResponse({"state": 0, "message": "token无效"})
