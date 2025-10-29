from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_product", views.create_product, name="create_product"),
    path("create_auction/<int:product_id>", views.create_auction, name="create_auction"),
    path("<int:product_id>", views.product_detail, name="product"),
    path("<int:product_id>/watchlist", views.watchlist, name='watchlist'),
    path("<int:auction_id>/bid", views.make_bid, name='make_bid'),
    path("watchlist", views.display_watchlist, name='display_watchlist'),
    path("categories", views.categories_view, name='categories'),
    path("categories/<str:category_name>", views.category_detail, name="category_detail")
]
