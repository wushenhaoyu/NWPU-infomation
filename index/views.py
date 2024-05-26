from django.utils import timezone

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
# Create your views here.
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from index.models import User,Patient,PatientInHospital,PatientOutHospital
from django.http import JsonResponse
from django.core.paginator import Paginator
def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')

def main_view(request):
    return render(request, 'main.html')

def patientInHospital_view(request):
    return render(request, 'patientInHospital.html')

def patientOutHospital_view(request):
    return render(request, 'patientOutHospital.html')

def in_view(request):
    return render(request, 'in.html')

def out_view(request):
    return render(request, 'out.html')

from django.http import JsonResponse
from .models import Patient, PatientInHospital

def get_patient_in_hospital(request):
    # 获取请求参数
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('pageSize', 10))

    # 使用Paginator创建分页对象
    patients_in_hospitals = PatientInHospital.objects.all().select_related('patient')
    paginator = Paginator(patients_in_hospitals, page_size)

    # 获取当前页的对象
    page_objects = paginator.page(page)

    # 转换为需要的字典格式
    data = [{'id': obj.id, 'username': obj.patient.name, 'age': obj.patient.age, 'gender': obj.patient.gender, 'IDcard': obj.patient.IDcard, 'timeInHospital': obj.timeInHospital.strftime('%Y-%m-%d %H:%M:%S')} for obj in page_objects.object_list]

    # 返回JSON响应，包括总页数和当前页数据
    return JsonResponse({
        'data': data,
        'total': paginator.count,
        'pages': paginator.num_pages,
        'currentPage': page,
        'code':200
    }, safe=False)

def get_patient_out_hospital(request):
    # 获取请求参数
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('pageSize', 10))

    # 使用Paginator创建分页对象
    patients_out_hospitals = PatientOutHospital.objects.all().select_related('patient')
    paginator = Paginator(patients_out_hospitals, page_size)

    # 获取当前页的对象
    page_objects = paginator.page(page)

    # 转换为需要的字典格式
    data = [{'id': obj.id, 'username': obj.patient.name, 'age': obj.patient.age, 'gender': obj.patient.gender, 'IDcard': obj.patient.IDcard, 'timeInHospital': obj.timeInHospital.strftime('%Y-%m-%d %H:%M:%S'), 'TimeOutHospital': obj.TimeOutHospital.strftime('%Y-%m-%d %H:%M:%S')} for obj in page_objects.object_list]

    # 返回JSON响应，包括总页数和当前页数据
    return JsonResponse({
        'data': data,
        'total': paginator.count,
        'pages': paginator.num_pages,
        'currentPage': page,
        'code':200
    }, safe=False)

def inHospital(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')
        IDcard = data.get('IDcard')
    # 检查患者是否存在
        try:
            patient = Patient.objects.get(name=name, age=age, IDcard=IDcard, gender=gender)

            # 检查患者是否已经在住院
            if PatientInHospital.objects.filter(patient=patient).exists():
                return JsonResponse({'status': 0, 'message': '已经住院了'})  # 或者返回错误消息

        except ObjectDoesNotExist:
            # 如果患者不存在，创建新的患者
            patient = Patient.objects.create(name=name, age=age, IDcard=IDcard, gender=gender)
        # 创建住院记录
            patient_in_hospital = PatientInHospital.objects.create(patient=patient, timeInHospital=timezone.now())

            return JsonResponse({'status': 1, 'message': '成功住院'})  # 或者返回错误消息
    else:
        return JsonResponse({'status': 0, 'message': '请求有误'})

def outHospital(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')
        IDcard = data.get('IDcard')

        # 检查患者是否存在
        try:
            patient = Patient.objects.get(name=name, age=age, IDcard=IDcard, gender=gender)

            # 检查患者是否在住院
            if not PatientInHospital.objects.filter(patient=patient).exists():
                return JsonResponse({'status': 0, 'message': '患者尚未住院'})

            # 获取患者的住院记录
            patient_in_hospital = PatientInHospital.objects.get(patient=patient)

            # 出院操作
            patient_in_hospital.OutHospital() # 假设你有一个这样的方法在PatientInHospital模型中
            patient_in_hospital.save()

            return JsonResponse({'status': 1, 'message': '成功出院'})

        except ObjectDoesNotExist:
            return JsonResponse({'status': 0, 'message': '患者不存在'})

    else:
        return JsonResponse({'status': 0, 'message': '请求有误'})


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        print(username, password)
        try:
            user = User.objects.get(userName=username)
            if password == user.password:
                return JsonResponse({'status': 1, 'message': 'Valid credentials'})
            else:
                return JsonResponse({'status': 0, 'message': 'Incorrect password'})
        except User.DoesNotExist:
            return JsonResponse({'status': 0, 'message': 'User not found'})
    else:
        return JsonResponse({'status': 0}, status=405)



@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        print(username, password)
        if User.objects.filter(userName=username).exists():
            return JsonResponse({'status': 0, 'message': 'Username already exists'})

        new_user = User.objects.create(userName=str(username), password=str(password))
        return JsonResponse({'status': 1, 'message': 'Registration successful'})
    else:
        return JsonResponse({'status': 0, 'message': 'Invalid request method'}, status=405)







