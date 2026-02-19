from django.shortcuts import render

# from django.http import HttpResponse

from .models import Product


def index(request):
    # return HttpResponse("Just to test")
    slogan = "- A tuto shop (Home page)"
    products = Product.objects.all()
    return render(request, "index.html", {"slogan": slogan, "produits": products})
