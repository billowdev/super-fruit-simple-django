from django.shortcuts import render
from django.http import HttpResponse
# HttpResponse คือ ฟังก์ชันสำหรับทำให้โชว์ข้อความหน้าเว็บได้

def Home(request):
	product1 = 'ทุเรียน'
	product2 = 'แอปเปิล'
	product3 = 'มังคุด'

	context = {'product1':product1, 'product2':product2, 'product3':product3}
	return render(request, 'myapp/home.html', context)


def About(request):
	return render(request, 'myapp/about.html')

def Contact(request):
	return render(request, 'myapp/contact.html')

def Apple(request):
	return render(request, 'myapp/apple.html')