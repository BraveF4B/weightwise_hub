from django.contrib import admin
from .models import Category, Product, Review, BrandReview, Newsletter

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'in_stock', 'is_featured']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['category', 'in_stock', 'is_featured']

    from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'product', 'rating', 'approved', 'created_at']
    list_filter = ['approved', 'rating']

    from .models import BrandReview

@admin.register(BrandReview)
class BrandReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'rating', 'approved', 'created_at']
    list_filter = ['approved', 'rating']

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at']
