from django.shortcuts import render,get_object_or_404
from .models import Product
from .models import CartItem

# Create your views here.

from django.http import HttpResponse
from django.template import loader

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())



    

def about(request):
    template = loader.get_template('about.html')
    return HttpResponse(template.render())

def contact(request):
    template = loader.get_template('contact.html')
    return HttpResponse(template.render())

def user(request):
    template = loader.get_template('user_page.html')
    return HttpResponse(template.render())

# def cart(request):
#     template = loader.get_template('cart.html')
#     return HttpResponse(template.render())

# def login(request):
#     template = loader.get_template('login.html')
#     return HttpResponse(template.render())

def checkout(request):
    template = loader.get_template('checkout.html')
    return HttpResponse(template.render())

def address(request):
    template = loader.get_template('address_page.html')
    return HttpResponse(template.render())

def orders(request):
    template = loader.get_template('orders_page.html')
    return HttpResponse(template.render())

def watch(request):
    template = loader.get_template('smartwatch.html')
    return HttpResponse(template.render())

def headphone(request):
    template = loader.get_template('headphone.html')
    return HttpResponse(template.render())

def speaker(request):
    template = loader.get_template('speaker.html')
    return HttpResponse(template.render())

def joystick(request):
    template = loader.get_template('joystick.html')
    return HttpResponse(template.render())

from django.shortcuts import render,redirect
from django.contrib.auth.models import User
# from.forms import SignupForm
from django.contrib.auth.hashers import make_password
from .forms import SignupForm
from django.contrib import messages
# from django.contrib.auth import authenticate, login
# def login(request):
#     if request.method == 'POST':       
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']   
#             user = authenticate(request, username=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, 'Login successful.')
#                 return redirect('index')
#             else:
#                 # Display an error message if authentication fails
#                 messages.error(request, 'Invalid username or password. Please try again.')
#         else:
#             # Display an error message if the form is invalid
#             messages.error(request, 'Invalid form submission. Please check your input.')        
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User(username=first_name, email=email)
            user.set_password(password)
            user.save()
            return redirect('user_login')  # Redirecting to the login page
    else:
        form = SignupForm()

    return render(request, 'register.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import LoginForm  # Make sure LoginForm is defined in forms.py

def user_login(request):
    error_message = None
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            # Retrieve the user object using the email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            # Authenticate with the username (not email) and password
            if user is not None:
                user = authenticate(username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("index")  # Replace 'index' with your desired redirect URL
                else:
                    error_message = "Invalid email or password."
            else:
                error_message = "Invalid email or password."
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form, "error_message": error_message})



from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import ContactDetail

def contact_view(request):
    if request.method == 'POST':
        form=ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contactlist')
        
    else:
        form=ContactForm()
    
    return render(request, 'contact.html', {'form':form})

def contactlist(request):
    detail=ContactDetail.objects.all()
    return render(request, 'contact.html', {'detail':detail})


# # ####################################33


# # views.py
# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .forms import UserUpdateForm, ProfileUpdateForm

# def my_account(request):
#     if request.method == 'POST':
#         user_form = UserUpdateForm(request.POST, instance=request.user)
#         profile_form = ProfileUpdateForm(request.POST, instance=request.user.userprofile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             return redirect('my_account')
#     else:
#         user_form = UserUpdateForm(instance=request.user)
#         profile_form = ProfileUpdateForm(instance=request.user.userprofile)

#     context = {
#         'user_form': user_form,
#         'profile_form': profile_form
#     }
#     return render(request, 'my_account.html', context)

   
def shop(request):
    gadgets=Product.objects.all()
    return render(request,'product-single.html',{'gadgets':gadgets})


def product_detail(request, product_id):
    thing=get_object_or_404(Product,pk=product_id)
    return render(request,'gadget_detail.html',{'thing':thing})

from django.contrib.auth.decorators import login_required

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_quantity = sum(item.quantity for item in cart_items)
    total_price = sum(item.total() for item in cart_items)
    return render(request, 'cart_page.html',{'cart_items':cart_items, 'total_quantity':total_quantity, 'total_price':total_price})   
    
from django.contrib import messages
from .models import CartItem

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart_item, created =CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required
def update_cart(request, cart_item_id):
    cart_item =get_object_or_404(CartItem, pk=cart_item_id, user=request.user)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if quantity.isdigit() and int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
    return redirect('cart')