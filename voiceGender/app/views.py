from gettext import translation
from django.shortcuts import render, get_object_or_404,redirect
from django.views import View
from .models import Contact, Product, Wishlist
from . import forms
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage 
from django.contrib import messages
from .forms import  CustomerRegistrationForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
import os
import time
import h5py
from . import test 
from django.db import transaction
#--------------------------
UPLOAD_FOLDER = 'uploads/'
# Create your views here.
class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    success_url = reverse_lazy('index')  

    def get_success_url(self):
        return self.success_url
def home(request):
    return render(request,'app/index.html')
def upload(request):
    if request.method == 'POST' and request.FILES['file']:
        audio_file = request.FILES['file']
        filename = os.path.join('app', 'uploads', 'recording.wav')

        with open(filename, 'wb') as f:
            for chunk in audio_file.chunks():
                f.write(chunk)

        time.sleep(1)  # Wait for 1 second to ensure the file is fully saved

        # Extract features and predict gender
        features = test.extract_feature(filename, mel=True).reshape(1, -1)
        model = test.create_model()
        model.load_weights("app/results/model.h5")
        male_prob = model.predict(features)[0][0]
        female_prob = 1 - male_prob
        gender = "male" if male_prob > female_prob else "female"

        # Convert NumPy float32 to Python float
        male_prob = float(male_prob)
        female_prob = float(female_prob)

        return JsonResponse({'result': gender, 'male_prob': male_prob, 'female_prob': female_prob})

#-------------------------------------------------------------
@transaction.atomic   
def contactUs(request):
    if request.method == 'POST':
        print("Form data:", request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        message = request.POST.get('message')
        print("Form data extracted:", name, email, phone_number, message)
        with transaction.atomic():
            contact = Contact.objects.create(
            name=name,
            email=email,
            phone_number=phone_number,
            message=message
        )
        print("Contact saved:", contact)
    return render(request, 'app/contactUs.html')

def aboutUs(request):
    return render(request,'app/aboutUs.html')
def Mtime(request):
    return render(request,'app/Mtime.html')
def Ftime(request):
    return render(request,'app/Ftime.html')

class CategoryView(View):
    def get(self,requset ,val):
        product = Product.objects.filter(category=val)
        title=Product.objects.filter(category=val).values('title')        
        return render(requset ,'app/category.html',locals())
class FCategoryView(View):
    def get(self,requset ,val):
        product = Product.objects.filter(category=val)
        title=Product.objects.filter(category=val).values('title')        
        return render(requset ,'app/Fcategory.html',locals())

class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/productD.html' ,locals())

class FProductDetail(View):
    def get(self ,requset,pk):
        product = Product.objects.get(pk=pk)
        return render(requset ,'app/FproductD.html',locals())    
        
class RegistrationView(View):
    def get(self, request):
        form = forms.CustomerRegistrationForm()
        return render(request, 'app/Registration.html', locals())
    def post(self, request):
        form = forms.CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User registered successfully.")
        else:
            messages.warning(request, "Invalid input data.")
        return render(request, 'app/Registration.html',locals())    
    

@login_required
def add_to_wishlist(request, product_id):
    product = Product.objects.get(pk=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    return redirect('productD', pk=product_id)

@login_required
def remove_from_wishlist(request, product_id):
    product = Product.objects.get(pk=product_id)
    wishlist = Wishlist.objects.get(user=request.user)
    wishlist.products.remove(product)
    return redirect('productD', pk=product_id)
   # return redirect('wishlist')

@login_required
def wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'app/wishlist.html', {'wishlist': wishlist})

def contact_success(request):
    return render(request, 'app/contact_success.html')
                      