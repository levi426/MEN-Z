from django.contrib import admin
from django.utils.html import format_html
from .models import Payment

def approve_payment(modeladmin, request, queryset):
    for payment in queryset:
        payment.status = 'approved'
        payment.save()

        payment.order.status = 'shipping'
        payment.order.track_order_status = 'shipping'
        payment.order.save(update_fields=['status', 'track_order_status'])

    modeladmin.message_user(request, f"{queryset.count()} payment(s) approved.")

approve_payment.short_description = "✓ Approve selected payments"


def reject_payment(modeladmin, request, queryset):
    for payment in queryset:
        payment.status = 'rejected'
        payment.save()

        payment.order.status = 'rejected'
        payment.order.track_order_status = '-'
        payment.order.save(update_fields=['status', 'track_order_status'])

    modeladmin.message_user(request, f"{queryset.count()} payment(s) rejected.")

reject_payment.short_description = "✗ Reject selected payments"


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'user', 'status', 'uploaded_at', 'image_preview')
    list_filter = ('status', 'uploaded_at')
    search_fields = ('order__id', 'user__email', 'status')
    readonly_fields = ('id', 'user', 'uploaded_at', 'image_preview')

    fields = ('id', 'order', 'user', 'image', 'image_preview', 'status', 'uploaded_at')

    actions = [approve_payment, reject_payment]  # ✅ IMPORTANT

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:300px; max-height:300px;" />',
                obj.image.url
            )
        return "No image"

    image_preview.short_description = "Image Preview"