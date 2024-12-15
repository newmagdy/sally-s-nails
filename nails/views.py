from django.shortcuts import render

# Create your views here.
def home(request):
    # You can pass any context here if needed, for now, it's just rendering a template
    return render(request, 'home.html')