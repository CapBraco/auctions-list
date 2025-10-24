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
]
