from django.contrib import admin
from .models import Product, CarouselImage, MeasurementImage, Order, OrderItem

# Register Product Model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'photo']

# Register CarouselImage Model
@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'alt_text']
    search_fields = ['alt_text']

# Register MeasurementImage Model
@admin.register(MeasurementImage)
class MeasurementImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'uploaded_at']

# Register Order Model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'created_at']

# Register OrderItem Model
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'price']
