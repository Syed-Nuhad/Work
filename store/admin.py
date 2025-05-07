from django.contrib import admin
from .models import Product, Variation, ReviewRating, ProductGallery
import admin_thumbnails

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'selling_price', 'cost_price', 'price', 'sold', 'stock', 'single_product_profit_display','category','single_product_profit_display', 'total_profit_display' 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductGalleryInline]
    readonly_fields = ['single_product_profit_display', 'total_profit_display']
    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))
        if obj and obj.sold > 0:
            fields += ['single_product_profit_display', 'total_profit_display']
        return fields

    def single_product_profit_display(self, obj):
        profit = obj.single_product_profit
        return f"${profit}" if profit is not None else "N/A"

    single_product_profit_display.short_description = "Single Product Profit"

    def total_profit_display(self, obj):
        total = obj.total_profit
        return f"${total}" if total is not None else "N/A"

    total_profit_display.short_description = "Total Profit"

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value')

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)
