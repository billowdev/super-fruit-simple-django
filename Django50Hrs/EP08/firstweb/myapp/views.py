from django.shortcuts import render
from django.http import HttpResponse
from .models import Allproduct
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
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

def AddProduct(request):
	if request.method == 'POST' and request.FILES['imageupload']:
		data = request.POST.copy()
		name = data.get('name')
		price = data.get('price')
		detail = data.get('detail')
		imageurl = data.get('imageurl')
		quantity = data.get('quantity')
		unit = data.get('unit')

		new = Allproduct()
		new.name = name
		new.price = price
		new.detail = detail
		new.imageurl = imageurl
		new.quantity = quantity
		new.unit = unit
		

		############ Save Image ############
		file_image = request.FILES['imageupload']
		file_image_name = request.FILES['imageupload'].name.replace(' ', '')
		print("FILE_IMAGE: ", file_image)
		print("IMAGE_NAME: ", file_image_name)
		fs = FileSystemStorage()
		filename = fs.save(file_image_name, file_image)
		upload_file_url = fs.url(filename)
		new.image = upload_file_url[6:] # slide url -> media/picture.jpg -> picture.jpg
		new.save()
		####################################

	return render(request, 'myapp/addproduct.html')

def Product(request):
	product = Allproduct.objects.all() # ดึงข้อมูลมากทั้งหมด
	product = product.order_by('id').reverse()
	context = {'product':product}
	return render(request, 'myapp/allproduct.html', context)

def Register(request):
	if request.method == 'POST':
		data = request.POST.copy()
		first_name = data.get('first_name')
		last_name = data.get('last_name')
		email = data.get('email')
		password = data.get('password')

		newuser = User()
		newuser.username = email
		newuser.email = email
		newuser.first_name = first_name
		newuser.last_name = last_name
		newuser.set_password(password)
		newuser.save() 

	return render(request, 'myapp/register.html')
