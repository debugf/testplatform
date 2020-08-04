# projects/views.py
from django.http import JsonResponse
from django.views import View
from django.core.paginator import Paginator

from projects.forms import CreateForm, UpdateForm
from projects.models import Projects
from utils.common import result, removeEmpty
from utils.jwt_permission_required import auth_permission_required


class CreateListView(View):
    # 分页 + 项目名模糊查询
    @auth_permission_required("class_func")
    def get(self, request):
        result["message"] = "查询成功"
        result["success"] = True
        page = request.GET.get("page", 1)
        size = request.GET.get("size", 10)
        name = request.GET.get("name", "")
        projects = Projects.objects.filter(is_delete=False, name__contains=name)
        projectss = Paginator(projects, size)
        project_list = []
        for project in projectss.page(page):
            project_list.append({
                'id': project.id,
                'name': project.name,
                'leader': project.leader,
                'tester': project.tester,
                'programer': project.programer,
                'publish_app': project.publish_app,
                'desc': project.desc
            })
        result["details"] = {
            "records": project_list,
            "pages": projectss.num_pages,
            "total": projectss.count
        }
        # JsonResponse第一个参数默认只能为dict字典，如果设为其他类型，需要将safe设为False
        return JsonResponse(result, safe=False, status=200)

    # 创建数据
    @auth_permission_required("class_func")
    def post(self, request):
        result["message"] = "保存失败"
        result["success"] = False
        result["details"] = None
        json_data = request.body.decode('utf-8')
        if json_data:
            python_data = eval(json_data)
            data = CreateForm(python_data)
            if data.is_valid():
                print(data.cleaned_data)
                Projects.objects.create(**data.cleaned_data)
                result["message"] = "保存成功"
                result["success"] = True
                result["details"] = data.cleaned_data
                return JsonResponse(result, status=200)
            else:
                result["details"] = data.errors
                return JsonResponse(result, status=400)
        return JsonResponse(result, status=500)


class UpdateDeleteView(View):
    # 更新数据
    @auth_permission_required("class_func")
    def put(self, request, pk):
        result["message"] = "更新失败"
        result["success"] = False
        result["details"] = None
        ret = Projects.objects.filter(id=pk, is_delete=False).values("id")
        if ret:
            json_data = request.body.decode('utf-8')
            if json_data:
                python_data = eval(json_data)
                data = UpdateForm(python_data)
                if data.is_valid():
                    a = Projects.objects.filter(name=python_data["name"]).values("id").first()
                    if not a or a["id"] == pk:
                        d = removeEmpty(data.cleaned_data)
                        Projects.objects.filter(id=pk).update(**d)
                        result["message"] = "更新成功"
                        result["success"] = True
                        result["details"] = d
                        return JsonResponse(result, status=200)
                    else:
                        result["details"] = "该项目名已存在"
                        return JsonResponse(result, status=400)
                else:
                    result["details"] = data.errors
                    return JsonResponse(result, status=400)
            return JsonResponse(result, status=500)
        else:
            result["details"] = "项目不存在"
            return JsonResponse(result, status=400)

    # 逻辑删除
    @auth_permission_required("class_func")
    def delete(self, request, pk):
        result["message"] = "删除失败"
        result["success"] = False
        result["details"] = None
        ret = Projects.objects.filter(id=pk, is_delete=False).values("id").first()
        if ret:
            project = Projects.objects.get(id=pk)
            project.is_delete = True
            project.save()
            result["message"] = "删除成功"
            result["success"] = True
            return JsonResponse(result, status=200)
        result["details"] = "项目不存在"
        return JsonResponse(result, status=400)

# 获取id和name
@auth_permission_required("func")
def names(reuqest):
    result["message"] = "查询成功"
    result["success"] = True
    projects = Projects.objects.filter(is_delete=False).values("id", "name")
    project_list = []
    for project in projects:
        project_list.append({
            'id': project["id"],
            'name': project["name"],
        })
    result["details"] = project_list
    return JsonResponse(result, safe=False, status=200)
