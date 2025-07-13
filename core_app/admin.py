from django.contrib import admin
from .models import Product,Review
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at')
    search_fields = ('name',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    search_fields = ('product__name', 'user__username')
    list_filter = ('rating', 'created_at')

admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
