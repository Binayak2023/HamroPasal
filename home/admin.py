from django.contrib import admin
from .models import Category, Product, MyCart, OrderPlaced, Contact, SubscriptionEmail, SubCategory, BannerContent, SlideContent, PromoCode, PromoCodeDiscount
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug']

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'title']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','category', 'sub_category', 'weight','available_quantity', 'selling_price', 'return_policy', 'tags', 'modified_date']
    search_fields = ['name__contains']
    # list_filter = ['available_quantity']
    class Media:
        js = ('js/tinyinject.js',)

@admin.register(MyCart)
class MyCartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'date_created']

@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'customer_info', 'product', 'product_info', 'quantity', 'total_price', 'ordered_date', 'unique_order_id', 'order_status']
    search_fields = ['unique_order_id__iexact']

    def customer_info(self, obj):
        link = reverse('admin:registration_customer_change', args=[obj.customer.id])
        return format_html('<a href="{}">{}</a>', link, obj.customer.full_name)

    def product_info(self, obj):
        link = reverse('admin:home_product_change', args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', link, obj.product.name)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['sno', 'full_name', 'email', 'preference', 'message', 'created_at']
    
@admin.register(SubscriptionEmail)
class SubscriptionEmailAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'subscribed_at']

@admin.register(SlideContent)
class SlideContentAdmin(admin.ModelAdmin):
    list_display = ['id', 'small_title', 'main_title', 'third_title','button_text', 'updated_at', 'created_at']

@admin.register(BannerContent)
class BannerContentAdmin(admin.ModelAdmin):
    list_display = ['id', 'small_title', 'main_title', 'third_title', 'button_text', 'updated_at', 'created_at']

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'promo_code_text', 'promo_code_discount', 'updated_at', 'created_at']

@admin.register(PromoCodeDiscount)
class PromoCodeDiscountPriceAdmin(admin.ModelAdmin):
    list_display = ['id', 'discount_price']