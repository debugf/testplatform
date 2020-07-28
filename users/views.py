from django.http import JsonResponse

from utils.jwt_permission_required import auth_permission_required


@auth_permission_required('users.select_user')
def user(request):
    if request.method == 'GET':
        _jsondata = {
            "user": "ops-coffee",
            "site": "https://ops-coffee.cn"
        }

        return JsonResponse({"state": 1, "message": _jsondata})
    else:
        return JsonResponse({"state": 0, "message": "Request method 'POST' not supported"})