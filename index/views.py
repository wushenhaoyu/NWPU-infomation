from django.shortcuts import render
# Create your views here.
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from index.models import User,Patient,PatientInHospital,PatientOutHospital
from django.http import JsonResponse
def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')




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







