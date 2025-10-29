from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from datetime import datetime
from django.utils import timezone
from .forms import *

from .models import User, Category, Product, Auction, Bid, Comment, Like, Transaction


def index(request):
    products = Product.objects.all().order_by('-created_at')
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
    auction = product.auction
    highest_bid = Bid.objects.filter(auction=auction).order_by('-amount').first()
    highest_bidder = highest_bid.user if highest_bid else None


    user_liked = False
    if request.user.is_authenticated:
        user_liked =Like.objects.filter(user=request.user, product=product).exists()


    comments = Comment.objects.filter(product=product).order_by('-created_at')

    comment_form = CommentForm(prefix='comment')
    auction_form = MyAuctionStatusForm(prefix='auction', instance=auction)

    if request.method == 'POST':

        if not request.user.is_authenticated:
            return redirect('login')
        
        if 'comment-submit' in request.POST:
            comment_form = CommentForm(request.POST, prefix='comment')
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.product = product
                comment.save()
                messages.success(request, 'Comment added successfully.')
                return redirect('product', product_id=product.id)
        
        elif 'auction-submit' in request.POST:
            auction_form = MyAuctionStatusForm(request.POST, prefix='auction', instance=auction)
            if auction_form.is_valid():
                old_status = auction.auction_status
                auction = auction_form.save(commit=False)

                if old_status != 'SO' and auction.auction_status == 'SO' and highest_bidder:
                    Transaction.objects.create(
                        auction=auction,
                        buyer=highest_bidder,
                        seller=product.user,
                        final_price=auction.current_price
                    )
                auction.save()
                messages.success(request, 'Status updated.')
                return redirect('product', product_id=product.id)   

    return render(request, "auctions/product.html",{
        "product": product,
        'user_liked': user_liked,
        "auction": auction,
        "comments": comments,
        "highest_bid": highest_bid,
        'comment_form': comment_form,
        'auction_form': auction_form
    })

def create_product(request):
    if request.method == 'POST':
        form = MyProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            form.save()
            return redirect('create_auction', product_id=product.id)
    else:
        form = MyProductForm()

    return render(request, 'auctions/create_product.html', {
        'form': form
        })

def create_auction(request, product_id):
        product = Product.objects.get(pk=product_id)

        if request.method == 'POST':
            form = MyAuctionForm(request.POST)
            if form.is_valid():
                auction = form.save(commit=False)
                auction.product = product
                if not auction.current_price:
                    auction.current_price = auction.starting_price
                auction.user = request.user
                auction.save()
                messages.success(request, f"Product '{product.name}' created successully.")
            return redirect('product', product_id)
        else:
            form = MyAuctionForm(initial={'product':product})

        return render(request, "auctions/create_auction.html", {
            "form": form,
            'product': product
        })
@login_required
def watchlist(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        like, created = Like.objects.get_or_create(user=request.user, product=product)
        if created:
            messages.success(request, f'Added "{product.name}" to your watchlist.') 
        else:
            like.delete()
            messages.info(request, f"Removed '{product.name}' from your watchlist.")

    return redirect('product', product_id=product.id)

@login_required
def make_bid(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    if request.method == 'POST':
        amount = request.POST.get('bid')
        if not amount:
            messages.error(request, 'Please enter a bid amount.')
            return redirect('product', product_id = auction.product.id)
        if auction.current_price <= float(amount):
            auction.current_price = float(amount)
            auction.save()

            Bid.objects.create(
            auction=auction,
            user=request.user,
            amount=amount
            )
            messages.success(request, f'Bid placed: ${amount}')
        else:
            messages.warning(request, 'Your bid must be higher than the current price')
    return redirect('product', product_id=auction.product.id)

@login_required
def display_watchlist(request):
    liked = Like.objects.filter(user=request.user).order_by('-created_at')
    user_bids = Bid.objects.filter(user=request.user).select_related('auction__product').order_by("-created_at")

    bid_products = {bid.auction.product for bid in user_bids}

    return render(request, 'auctions/watchlist.html', {
        "liked":liked,
        "bid_products": bid_products,
        "user_bids":user_bids
    })

def categories_view(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category_detail(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    products = Product.objects.filter(categories=category).distinct()

    return render(request, "auctions/category_detail.html",{
        "category": category,
        "products": products
    })
    