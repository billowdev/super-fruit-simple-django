from django.shortcuts import render
from django.http import HttpResponse
# HttpResponse คือ ฟังก์ชันสำหรับทำให้โชว์ข้อความหน้าเว็บได้

def Home(request):
	return render(request, 'myapp/home.html')