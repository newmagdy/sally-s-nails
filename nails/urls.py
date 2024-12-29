# nails/urls.py
from django.urls import path
from . import views
from .views import home, signin, signup, signout
#from .views import home 
#from django.conf.urls.static import static

urlpatterns = [
    
    path('', views.home, name='home'),
    path('signin/', signin, name='signin'),
    path('signup/', signup, name='signup'),
    path('logout/', signout, name='logout'),
    path('cart/', views.cart, name='cart'), 
    path('payment/', views.payment, name='payment'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),  # New product detail view
    path('measurement/', views.measurement, name='measurement'),
]

