from django.contrib import admin
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from .models import Product, Variation, ReviewRating, ProductGallery
import admin_thumbnails

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


class VariationInline(admin.TabularInline):
    model = Variation
    fields = ['variation_category', 'variation_value', 'is_active']

def export_product_pdf(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="products_table.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - 2 * cm
    x_list = [1 * cm, 5 * cm, 8 * cm, 10 * cm, 12 * cm, 14 * cm, 16 * cm, 18 * cm]

    # Header
    p.setFont("Helvetica-Bold", 10)
    p.drawString(x_list[0], y, "Name")
    p.drawString(x_list[1], y, "Category")
    p.drawString(x_list[2], y, "Price")
    p.drawString(x_list[3], y, "Cost")
    p.drawString(x_list[4], y, "Selling")
    p.drawString(x_list[5], y, "Stock")
    p.drawString(x_list[6], y, "Sold")
    p.drawString(x_list[7], y, "Profit")
    y -= 15

    p.setFont("Helvetica", 9)
    grand_total = 0

    for product in queryset:
        if y < 2 * cm:
            p.showPage()
            y = height - 2 * cm

            # Redraw headers on new page
            p.setFont("Helvetica-Bold", 10)
            p.drawString(x_list[0], y, "Name")
            p.drawString(x_list[1], y, "Category")
            p.drawString(x_list[2], y, "Price")
            p.drawString(x_list[3], y, "Cost")
            p.drawString(x_list[4], y, "Selling")
            p.drawString(x_list[5], y, "Stock")
            p.drawString(x_list[6], y, "Sold")
            p.drawString(x_list[7], y, "Profit")
            y -= 15
            p.setFont("Helvetica", 9)

        profit = product.total_profit or 0
        grand_total += profit

        p.drawString(x_list[0], y, str(product.product_name)[:15])
        p.drawString(x_list[1], y, str(product.category.category_name)[:10])
        p.drawString(x_list[2], y, f"${product.price}")
        p.drawString(x_list[3], y, f"${product.cost_price}")
        p.drawString(x_list[4], y, f"${product.selling_price}")
        p.drawString(x_list[5], y, str(product.stock))
        p.drawString(x_list[6], y, str(product.sold))
        p.drawString(x_list[7], y, f"${profit}")
        y -= 15

    # Add Grand Total at the end
    y -= 15
    p.setFont("Helvetica-Bold", 11)
    p.drawString(x_list[6], y, "Grand Total:")
    p.drawString(x_list[7], y, f"${grand_total}")

    p.save()
    return response
export_product_pdf.short_description = "Export selected products as PDF"

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'selling_price', 'cost_price', 'price', 'sold', 'stock', 'single_product_profit_display','category','single_product_profit_display', 'total_profit_display', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    actions = [export_product_pdf]
    inlines = [ProductGalleryInline, VariationInline]
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
