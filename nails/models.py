from django.db import models
from django.utils.timezone import now

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)  # Product name
    photo = models.ImageField(upload_to='products/')  # ImageField for product photos
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(default="No description available")  # new

    def __str__(self):
        return self.name


class CarouselImage(models.Model):
    image = models.ImageField(upload_to='carousel/', null=True, blank=True)
    alt_text = models.CharField(max_length=255)

    def __str__(self):
        return self.alt_text


class Order(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    shipping_method = models.CharField(max_length=50, default="Standard Shipping")
    payment_method = models.CharField(max_length=50, default="Cash on Delivery")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    measurements = models.JSONField(default=list)
    product_name = models.CharField(max_length=100, default="")

    def __str__(self):
        return f"Order {self.id} - {self.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product_name} (x{self.quantity})"


class MeasurementImage(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='measurement_images/')
    uploaded_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.title or "Untitled Image"
