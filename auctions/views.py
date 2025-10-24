from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime
from django.utils import timezone

from .models import User, Product, Auction, Bid, Comment, Like, Transaction


def index(request):
    products = Product.objects.all()
    return render(request, "auctions/index.html",{'products':products})
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, "auctions/product.html",{
        "product": product
    })

def create_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category = request.POST.get('category')
        image = request.FILES.get('image')

        if name and description and image:
            product = Product.objects.create(
                user= request.user,
                name=name,
                description=description,
                category=category,
                image=image
                )
        return redirect('create_auction', product_id=product.id)
    return render(request, 'auctions/create_product.html')
    
def create_auction(request, product_id):
        product = Product.objects.get(pk=product_id)

        if request.method == 'POST':
            starting_price = request.POST.get('starting_price') 
            auction_status = request.POST.get('auction_status')
            end_time_str = request.POST.get('end_time')
            end_time = datetime.fromisoformat(end_time_str)
            end_time = timezone.make_aware(end_time)

            Auction.objects.create(
                product= product,
                starting_price= starting_price,
                current_price = starting_price,
                auction_status = auction_status,
                end_time=end_time,
                )
            return redirect('index')
        return render(request, "auctions/create_auction.html", {
            "product": product
        })



        

