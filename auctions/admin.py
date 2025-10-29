from django.contrib import admin
from auctions.models import User, Category, Product, Auction, Bid, Comment, Like, Transaction

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    pass
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
class ProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'description', 'created_at', 'updated_at']
class AuctionAdmin(admin.ModelAdmin):
    list_display = ['product', 'starting_price', 'current_price', 'auction_status', 'start_time', 'end_time']
class BidAdmin(admin.ModelAdmin):
    list_display = ['auction', 'user', 'amount', 'created_at']
class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'comment', 'created_at']

admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like)