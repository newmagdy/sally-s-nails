from django.contrib import admin
from .models import Product
from .models import CarouselImage
from .models import MeasurementImage

# Register your models here.
admin.site.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'photo']

    admin.site.register(CarouselImage)
    

    class CarouselImageAdmin(admin.ModelAdmin):
       list_display = ['id', 'image', 'alt_text']
    search_fields = ['alt_text']

admin.site.register(MeasurementImage)