from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Task
from .models import Product, CarouselImage ,Order, OrderItem
#from .models import Order, OrderItem
from .models import MeasurementImage
from django.contrib import messages  # For the success alert
from decimal import Decimal, InvalidOperation
from django.shortcuts import render, get_object_or_404 #new


# Create your views here.

@login_required
def home(request):
    # Fetch tasks from the database
    tasks = Task.objects.all()  # Fetch all tasks from the database
    return render(request, 'nails/home.html', {'tasks': tasks})  # Pass tasks as context to the template

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after signing up
            return redirect('home')  # Redirect to home page after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'nails/signup.html', {'form': form})  # Render signup template with form

def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()  # Get the user object from the form
            login(request, user)  # Log in the user after successful authentication
            return redirect('home')  # Redirect to home page after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'nails/signin.html', {'form': form})  # Render signin template with form

def signout(request):
    logout(request)  # Log out the user
    return redirect('signin')  # Redirect to signin page after logging out
#def home(request):
    products = Product.objects.all()  # Fetch all products from the database
    return render(request, 'nails/home.html', {'products': products})
def cart(request):
    return render(request, 'nails/cart.html')
def payment(request):
    return render(request, 'nails/payment.html')
def measurement(request):
    return render(request, 'nails/measurement.html')



def payment(request):
    
    if request.method == 'POST':
        # Retrieve the form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        shipping_method = request.POST.get('shipping')
        total_price = request.POST.get("total_price")
        payment_method = request.POST.get('payment_method')
        card_number = request.POST.get("card_number", None)  # Optional for COD
        expiration_date = request.POST.get("expiration_date", None)
        cvv = request.POST.get("cvv", None)


        try:
            
            total_price = Decimal(total_price)
        except (ValueError, InvalidOperation):
            # Handle invalid decimal format
            messages.error(request, "Invalid total price. Please check the payment details.")
            return redirect('payment')  

        # Save the order to the database
        if payment_method == "cod":
          order = Order.objects.create(
            name=name,
            email=email,
            phone=phone,
            address=address,
            shipping_method=shipping_method,
            payment_method=payment_method,
            total_price=total_price,
        )
        
          # Save cart items into OrderItem model
        cart = request.session.get("checkoutCart", [])
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product_name=item["name"],
                price=item["price"],
                quantity=item["quantity"],
                measurements = request.POST.getlist('measurements[]')
            )
            # Clear the session cart
            
        request.session["checkoutCart"] = []
        


        # Success message
        messages.success(request, "Your order has been placed successfully!")
        return redirect('home')  # Redirect to your catalog or home page
    
    return render(request, 'nails/payment.html')

    

# View for the Home page
def home(request):
    # Fetch all products and carousel images from the database
    products = Product.objects.all()
    carousel_images = CarouselImage.objects.all()

    # Pass products and carousel images to the template
    return render(request, 'nails/home.html', {'products': products, 'carousel_images': carousel_images})
#new
# New product detail view
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)  # Get product by primary key
    return render(request, 'nails/product_detail.html', {'product': product})

def measurement(request):
    image = MeasurementImage.objects.last()  # Get the most recent image
    return render(request, 'nails/measurement.html', {'image': image})    