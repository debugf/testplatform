# projects/views.py
from django.http import JsonResponse
from django.views import View

from projects.forms import CreateForm
from projects.models import Projects
from utils.result import result

result["success"] = False


class CreateListView(View):

    def get(self, request):
        projects = Projects.objects.filter(is_delete=True)
        project_list = []
        for project in projects:
            project_list.append({
                'name': project.name,
                'leader': project.leader,
                'tester': project.tester,
                'programer': project.programer,
                'publish_app': project.publish_app,
                'desc': project.desc
            })
        # JsonResponse第一个参数默认只能为dict字典，如果设为其他类型，需要将safe设为False
        return JsonResponse(project_list, safe=False, status=200)

    def post(self, request):
        json_data = request.body.decode('utf-8')
        if json_data:
            python_data = eval(json_data)
            data = CreateForm(python_data)
            if data.is_valid():
                a = Projects.objects.create(**data.cleaned_data)
                print(a)
                result["message"] = "保存成功"
                result["success"] = True
                result["details"] = data.cleaned_data
                return JsonResponse(result, status=200)
            else:
                result["message"] = "保存失败"
                result["details"] = data.errors
                return JsonResponse(result, status=400)
        result["message"] = "保存失败"
        return JsonResponse(result, status=500)

