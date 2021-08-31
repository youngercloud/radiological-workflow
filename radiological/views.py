from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'index.html')


def order(request):
    return render(request, 'orders.html')


def booking(request):
    return render(request, 'booking.html')


