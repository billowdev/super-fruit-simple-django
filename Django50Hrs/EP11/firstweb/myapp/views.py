from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
# HttpResponse คือ ฟังก์ชันสำหรับทำให้โชว์ข้อความหน้าเว็บได้


def Home(request):
	product = Allproduct.objects.all().order_by('id').reverse()[:3] # ดึงข้อมูลมากทั้งหมด
	preorder = Allproduct.objects.filter(quantity__lte=0)
	context = {'product':product, 'preorder':preorder}
	return render(request, 'myapp/home.html', context)

def About(request):
	return render(request, 'myapp/about.html')

def Contact(request):
	return render(request, 'myapp/contact.html')

def Apple(request):
	return render(request, 'myapp/apple.html')

def AddProduct(request):

	if request.user.profile.usertype != 'admin':
		return redirect('home-page')

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

		# ยังไม่ใส่ try except เพื่อป้องกันการสมัครซ้ำ
		# + alert ไปหน้าสมัครว่าอีเมลนี้เคยสมัครแล้ว
		newuser = User()
		newuser.username = email
		newuser.email = email
		newuser.first_name = first_name
		newuser.last_name = last_name
		newuser.set_password(password)
		newuser.save()

		profile = Profile()
		profile.user = User.objects.get(username=email)
		
		# from django.contrib.auth import authenticate, login
		user = authenticate(username=email, password=password)
		login(request, user)

	return render(request, 'myapp/register.html')

def AddtoCart(request, pid):
	# localhost:8000/addtocart/3
	# {% url 'addtocart-page' pd.id %}
	# print('CURRENT USER', request.user)
	username = request.user.username
	user = User.objects.get(username=username)
	check = Allproduct.objects.get(id=pid)

	try:
		newcart = Cart.objects.get(user=user, productid=str(pid))
		# print("EXISTS: ", pcheck.exists())
		newquan = newcart.quantity + 1
		newcart.quantity = newquan
		calculate = newcart.price * newquan 
		newcart.total = calculate
		newcart.save()

		## update จำนวนของตระกร้าสินค้า ณ ตอนนี้
		count = Cart.objects.filter(user=user)
		count = sum([ c.quantity for c in count ])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()

		return redirect('allproduct-page')
	except:
		newcart = Cart()
		newcart.user = user
		newcart.productid = pid
		newcart.productname = check.name
		newcart.price = int(check.price)
		newcart.quantity = 1
		calculate = int(check.price) * 1
		newcart.total = calculate
		newcart.save()

		count = Cart.objects.filter(user=user)
		count = sum([ c.quantity for c in count ])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()

		return redirect('allproduct-page')

def MyCart(request):
	username = request.user.username
	user = User.objects.get(username=username)
	context = {}
	if request.method == 'POST':
		# ใช้สำหรับการลบเท่านั้น
		data = request.POST.copy()
		productid = data.get('productid')
		print('PID ', productid)
		item = Cart.objects.get(user=user, productid=productid)
		item.delete()
		context['status'] = 'delete'

		count = Cart.objects.filter(user=user)
		count = sum([ c.quantity for c in count ])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()

	mycart = Cart.objects.filter(user=user)
	context['mycart'] = mycart
	return render(request, 'myapp/mycart.html', context)