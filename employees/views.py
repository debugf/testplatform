# employees/views.py
import json

from django.http import JsonResponse

from employees.forms import EmployeeForm
from employees.models import Employees
from django.views import View

# django.views.View：自行调度['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']对应的视图函数
class EmployeesListCreateView(View):

    # get请求：获取全部员工数据
    def get(self, request):
        # Employees.objects.filter(is_delete=False)：
        #       Employees：数据模型
        #       objects：想要操作数据就得加上这个
        #       filter：条件查询某些数据，返回的是一个查询集
        #       is_delete=False：这个是数据库表中我们定义的字段，目的是查询所有没有被软删除的数据
        employees = Employees.objects.filter(is_delete=False)
        employee_list = []
        # 查询集不能直接返回，我们这里把它转为列表
        for employee in employees:
            employee_list.append({
                'id': employee.id,
                'ename': employee.ename,
                'jobnumber': employee.jobnumber,
                'create_time': employee.create_time
            })
        # JsonResponse：将数据以Json格式返回给前端
        # safe=False：JsonResponse第一个参数默认只能为dict字典，如果设为其他类型，需要将safe设为False，我们返回的是列表所以将safe设为False
        # status=200：响应码
        return JsonResponse(employee_list, safe=False, status=200)

    # post请求：创建员工信息
    def post(self, request):
        json_data = request.body.decode('utf-8')
        python_data = eval(json_data)
        employee_form = EmployeeForm(python_data)
        if employee_form.is_valid():
            employee = employee_form.save(commit=True)
            employee_form.cleaned_data["create_time"] = employee.create_time
            return JsonResponse(employee_form.clean(), status=201)
        else:
            return JsonResponse(employee_form.errors, safe=False, status=201)

class EmployeesRetrieveUpdateDestroyView(View):

    # 根据员工id获取该员工的详情数据，pk：接收前端传的id值
    def get(self, request, pk):
        # 查询id为pk，并且没有被软删除的员工信息，虽然数据只有一条，但filter()查出来的是查询集，所以用first()拿出第一条数据
        employee = Employees.objects.filter(id=pk, is_delete=False).first()
        # 如果查出不来的不为空
        if employee:
            # 转为字典
            dict = {"id": employee.id,
                    "ename": employee.ename,
                    "email": employee.email,
                    "jobnumber": employee.jobnumber,
                    "age": employee.age,
                    "sex": employee.sex,
                    "update_time": employee.update_time,
                    "create_time": employee.create_time
                    }
            # 返回给前端
            return JsonResponse(dict, status=200)
        # 否则，就是为空，数据库没有id为pk的数据
        else:
            return JsonResponse({"details": "数据不存在"}, status=200)

    # 更新某个员工全部信息
    def put(self, request, pk):
        # 很多校验都没做，所以这里直接用try来获取异常
        try:
            # 去数据库中查找要修改的员工id
            employee = Employees.objects.filter(id=pk, is_delete=False).first()
            # 如果为True，说明存在可以修改
            if employee:
                # 转码
                json_data = request.body.decode('utf-8')
                # 将json字符串转为Python中的字典
                python_data = eval(json_data)
                # 去数据库中查找要修改的工号是否已经存在，因为工号(jobnumber)有唯一约束
                jobnumber = Employees.objects.filter(jobnumber=python_data["jobnumber"]).first()
                # 如果要修改的工号不存在就可以修改，或者数据库中存在的工号是我们现在要改的这条数据也可以修改
                if jobnumber == None or jobnumber.id == pk:
                    # 给根据id查出来的数据employee进行赋值
                    employee.ename = python_data['ename']
                    employee.jobnumber = python_data['jobnumber']
                    employee.age = python_data['age']
                    employee.sex = python_data['sex']
                    employee.email = python_data['email']
                    # save()：赋值完成后保存
                    employee.save()
                    # 转为前端需要的数据
                    dict = {"id": employee.id,
                            "ename": employee.ename,
                            "email": employee.email,
                            "jobnumber": employee.jobnumber,
                            "age": employee.age,
                            "sex": employee.sex,
                            "update_time": employee.update_time,
                            "create_time": employee.create_time
                            }
                    # 返回Json给前端
                    return JsonResponse(dict, status=201)
                # 否则，剩下的结果是工号存在并且不是要修改的这条
                else:
                    return JsonResponse({"details": "工号已存在"}, status=201)
            # 否则，就是前端传的员工id不存在
            else:
                return JsonResponse({"details": "数据不存在"}, status=201)
        # 捕获异常赋值给e，捕获到的异常场都是因为我们没有做各种校验
        except Exception as e:
            return JsonResponse({"details": "数据错误", "error": str(e)}, status=400)

    # 更新某个员工的部分数据
    def patch(self, request, pk):
        # 很多校验都没做，所以这里直接用try来获取异常
        try:
            # 去数据库中查找前端传的员工id
            employee = Employees.objects.filter(id=pk, is_delete=False)
            # 如果为True，说明查出了数据，员工是存在的可以修改
            if employee:
                # 转码
                json_data = request.body.decode('utf-8')
                # 将json字符转为python中的字典
                python_data = eval(json_data)
                # 判断要修改的数据中有没有工号(jobnumber)，如果有就要做唯一校验
                if python_data.get("jobnumber"):
                    # 查询要修改的工号是否存在
                    jobnumber = Employees.objects.filter(jobnumber=python_data["jobnumber"]).first()
                    # 如果要修改的工号不存在就可以修改，或者数据库中存在的工号是我们现在要改的这条数据也可以修改
                    if jobnumber == None or jobnumber.id == pk:
                        employee.update(**python_data)
                        return JsonResponse({"details": "修改成功"}, status=201)
                    # 否则，剩下的结果是工号存在并且不是要修改的这条
                    else:
                        return JsonResponse({"details": "工号已存在"}, status=201)
                # 否则，就是不修改工号(jobnumber)，其他字段没有唯一约束，直接改就行
                else:
                    # 将根据id查出来的数据进行更新
                    employee.update(**python_data)
                    return JsonResponse({"details": "修改成功"}, status=201)
            # 否则，就是前端传的员工id不存在
            else:
                return JsonResponse({"details": "数据不存在"}, status=201)
        # 捕获异常赋值给e，捕获到的异常场都是因为我们没有做各种校验
        except Exception as e:
            return JsonResponse({"details": "数据错误", "error": str(e)}, status=400)

    # 根据某条员工数据
    def delete(self, request, pk):
        # 根据id查询要删除的员工，并且is_delete=False没有被软删除
        employee = Employees.objects.filter(id=pk, is_delete=False).first()
        # 如果要删除的员工存在
        if employee:
            # 进行软删除，is_delete我们在数据库中定义的软删除标记字段
            employee.is_delete = True
            employee.save()
            return JsonResponse({"details": "删除成功"}, status=201)
        # 否者，就是要删除的员工不存在
        else:
            return JsonResponse({"details": "数据不存在"}, status=200)


