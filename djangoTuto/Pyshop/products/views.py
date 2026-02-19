from django.shortcuts import render
from django.http import HttpResponse

from .models import Product


def index(request):
    # return HttpResponse("Hello world")
    products = Product.objects.all()
    return render(request, "index.html", {"produits": products})
