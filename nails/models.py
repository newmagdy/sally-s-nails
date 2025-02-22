from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=255, help_text="Enter the name of the task.")
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"


class Product(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(default="No description available")
    requires_measurements = models.BooleanField(default=False)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class CarouselImage(models.Model):
    image = models.ImageField(upload_to='carousel/', null=True, blank=True)
    alt_text = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return self.alt_text or "Carousel Image"

    class Meta:
        verbose_name = "Carousel Image"
        verbose_name_plural = "Carousel Images"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]
    SHIPPING_METHODS = [
        ('standard', 'Standard Shipping'),
        ('express', 'Express Shipping'),
    ]
    PAYMENT_METHODS = [
        ('cod', 'Cash on Delivery'),
        ('card', 'Credit Card'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    shipping_method = models.CharField(max_length=50, choices=SHIPPING_METHODS, default='standard')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS, default='cod')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    def calculate_total_price(self):
        total = sum(item.price * item.quantity for item in self.items.all())
        self.total_price = total
        self.save()

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    measurements = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity}in Order {self.order.id}"

    def save(self, *args, **kwargs):
        # Ensure the price is set from the product if not provided
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"


class MeasurementImage(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='measurement_images/')
    uploaded_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.title if self.title else "Untitled Image"

    class Meta:
        verbose_name = "Measurement Image"
        verbose_name_plural = "Measurement Images"