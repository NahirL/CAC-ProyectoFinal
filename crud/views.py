from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm


def home(request):
	return render(request, 'home.html', {})

def shop(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {'products': products})

def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def management(request):
    products = Product.objects.all()
    return render(request, 'management.html', {'products': products})

def categories(request):
    categories = Category.objects.all()
    return render(request, 'about.html', {'categories': categories})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("¡Has iniciado sesión!"))
            return redirect('home')
        else:
            messages.success(request, ("Hubo un error, por favor intente de nuevo"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request, ("¡Has cerrado sesión!"))
	return redirect('home')

def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# log in user
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("¡Te has registrado correctamente!"))
			return redirect('home')
		else:
			messages.success(request, ("¡Lo sentimos! Hubo un problema, por favor intente de nuevo"))
			return redirect('register')
	else:
		return render(request, 'register.html', {'form':form})


def add(request):
    name = request.POST["name"]
    price = request.POST["price"]
    category_str = request.POST["category"]
    description = request.POST["description"]
    image = request.FILES["image"]
    category, created = Category.objects.get_or_create(name=category_str)
    product = Product(name=name, price=price, category=category, description=description, image=image)
    product.save()
    messages.success(request, '¡Producto agregado!')
    return redirect('management')


def delete(request, id):
    product = Product.objects.filter(pk=id)
    product.delete()
    messages.success(request, '¡Producto eliminado!')
    return redirect('management')


def detalle(request, id):
    product = Product.objects.get(pk=id)
    return render(request, 'update.html', {'product': product})


def update(request, id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=id)
        name = request.POST['name']
        price = request.POST['price']
        category_str = request.POST['category']
        description = request.POST['description']
        nueva_imagen = request.FILES.get('image')
        # Actualiza los campos
        product.name = name
        product.price = price
        product.category, created = Category.objects.get_or_create(name=category_str)
        product.description = description
        # Verifica si se proporciona una nueva imagen
        if nueva_imagen:
            product.image = nueva_imagen
        # Guarda el producto actualizado
        product.save()
        messages.success(request, '¡Producto actualizado!')
        return redirect('management')
