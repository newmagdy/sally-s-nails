from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal, InvalidOperation
from django.db import transaction
import json
from .models import Task, Product, CarouselImage, Order, OrderItem, MeasurementImage
from django.contrib.admin.views.decorators import staff_member_required

# Home page view
@login_required
def home(request):
    products = Product.objects.all()
    carousel_images = CarouselImage.objects.all()
    return render(request, 'nails/home.html', {'products': products, 'carousel_images': carousel_images})

# User signup view
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'nails/signup.html', {'form': form})

# User login view
def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'nails/signin.html', {'form': form})

# User logout view
def signout(request):
    logout(request)
    return redirect('signin')

# Product detail view
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'nails/product_detail.html', {'product': product})

# Cart view
def cart(request):
    return render(request, 'nails/cart.html')

# Order history view (Added back)
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'nails/order_history.html', {'orders': orders})

# Payment view
@login_required
def payment(request):
    if request.method == 'POST':
        try:
            # Parse form data
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            shipping_method = request.POST.get('shipping', 'standard')
            payment_method = request.POST.get('payment_method', 'cod')
            total_price = Decimal(request.POST.get('total_price', '0.00'))
            cart_data = request.POST.get('cart_data', '[]')

            # Debugging output
            print("Payment Form Data:", {
                "name": name,
                "email": email,
                "phone": phone,
                "address": address,
                "shipping_method": shipping_method,
                "payment_method": payment_method,
                "total_price": total_price,
                "cart_data": cart_data,
            })

            # Validate cart data
            try:
                cart = json.loads(cart_data)
                if not cart:
                    raise ValueError("Cart data is empty or invalid.")
            except json.JSONDecodeError:
                messages.error(request, "Invalid cart data format.")
                return redirect('payment')

            # Validate form fields
            if not all([name, email, phone, address, total_price]):
                messages.error(request, "All fields are required.")
                return redirect('payment')

            # Save the order and order items
            with transaction.atomic():
                # Create order
                order = Order.objects.create(
                    user=request.user,
                    name=name,
                    email=email,
                    phone=phone,
                    address=address,
                    shipping_method=shipping_method,
                    payment_method=payment_method,
                    total_price=total_price,
                )

                # Save order items
                for item in cart:
                    product = Product.objects.get(id=item['product_id'])
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        price=Decimal(item['price']),
                        quantity=int(item['quantity']),
                        measurements=item.get('measurements', []),
                    )

                # Clear the cart
                request.session['cart'] = []
                messages.success(request, "Your order has been placed successfully!")
                return redirect('order_history')  # Redirects to order history after payment

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('payment')

    return render(request, 'nails/payment.html')

# Measurement view
def measurement(request):
    image = MeasurementImage.objects.last()  # Get the most recent image
    return render(request, 'nails/measurement.html', {'image': image})


# API to Return Cart Data as JSON
def cart_api(request):
    cart = request.session.get('cart', [])
    return JsonResponse({'cart': cart})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'nails/order_history.html', {'orders': orders})

@staff_member_required
def admin_orders(request):
    orders = Order.objects.filter(status='confirmed').order_by('-created_at')
    return render(request, 'nails/admin_orders.html', {'orders': orders})