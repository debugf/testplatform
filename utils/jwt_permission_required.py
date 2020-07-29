import jwt
from django.conf import settings
from django.http import JsonResponse
from users.models import Users

UserModel = Users

def auth_permission_required():
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            try:
                auth = request.META.get('HTTP_AUTHORIZATION').split()
            except AttributeError:
                return JsonResponse({"code": 401, "message": "没有权限"})
            # 用户通过 API 获取数据验证流程
            if auth[0].lower() == 'token':
                try:
                    dict = jwt.decode(auth[1], settings.SECRET_KEY, algorithms=['HS256'])
                    username = dict.get('data').get('username')
                    print(username)
                except jwt.ExpiredSignatureError:
                    return JsonResponse({"status_code": 401, "message": "token 已过期"})
                except jwt.InvalidTokenError:
                    return JsonResponse({"status_code": 401, "message": "token 无效"})
                except Exception as e:
                    return JsonResponse({"status_code": 401, "message": "无法获取用户对象"})
                try:
                    UserModel.objects.get(username=username)
                except UserModel.DoesNotExist:
                    return JsonResponse({"status_code": 401, "message": "用户不存在"})
            else:
                return JsonResponse({"status_code": 401, "message": "不支持身份验证类型"})
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator