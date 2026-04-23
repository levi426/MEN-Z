from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Order, OrderItem, RefundRequest


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ('product_name', 'price_at_purchase', 'quantity', 'get_subtotal')
    readonly_fields = ('product_name', 'price_at_purchase', 'quantity', 'get_subtotal', 'content_type', 'object_id')
    can_delete = True
    extra = 0

    def get_subtotal(self, obj):
        return f"Rs {obj.calculate_subtotal():.2f}"
    get_subtotal.short_description = "Subtotal"


def mark_as_paid(modeladmin, request, queryset):
    for order in queryset:
        order.status = 'paid'
        order.track_order_status = 'payment received'
        order.save(update_fields=['status', 'track_order_status'])
    modeladmin.message_user(request, f"{queryset.count()} order(s) marked as PAID.")
mark_as_paid.short_description = "Mark selected orders as Paid"


def mark_as_processing(modeladmin, request, queryset):
    for order in queryset:
        order.status = 'processing'
        order.track_order_status = 'processing'
        order.save(update_fields=['status', 'track_order_status'])
    modeladmin.message_user(request, f"{queryset.count()} order(s) marked as PROCESSING.")
mark_as_processing.short_description = "Mark as Processing"


def mark_as_shipped(modeladmin, request, queryset):
    for order in queryset:
        order.status = 'shipped'
        order.track_order_status = 'shipped'
        order.save(update_fields=['status', 'track_order_status'])
    modeladmin.message_user(request, f"{queryset.count()} order(s) marked as SHIPPED.")
mark_as_shipped.short_description = "Mark as Shipped"


def mark_as_delivered(modeladmin, request, queryset):
    for order in queryset:
        order.status = 'delivered'
        order.track_order_status = 'delivered'
        order.save(update_fields=['status', 'track_order_status'])
    modeladmin.message_user(request, f"{queryset.count()} order(s) marked as DELIVERED.")
mark_as_delivered.short_description = "Mark as Delivered"


def mark_as_cancelled(modeladmin, request, queryset):
    for order in queryset:
        order.status = 'cancelled'
        order.track_order_status = 'cancelled'
        order.save(update_fields=['status', 'track_order_status'])
    modeladmin.message_user(request, f"{queryset.count()} order(s) marked as CANCELLED.")
mark_as_cancelled.short_description = "Mark as Cancelled"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user_email', 'order_date', 'status', 'track_order_status', 'total_amount', 'get_item_count')
    list_filter = ('status', 'track_order_status', 'order_date')
    search_fields = ('user__email', 'user__username')
    inlines = [OrderItemInline]
    readonly_fields = ('order_date', 'total_amount', 'get_order_items_summary')

    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'order_date', 'status', 'track_order_status', 'total_amount', 'loyalty_points_earned')
        }),
        ('Shipping Details', {
            'fields': ('shipping_address',)
        }),
        ('Items Summary', {
            'fields': ('get_order_items_summary',),
            'classes': ('wide',)
        }),
    )

    actions = [
        mark_as_paid,
        mark_as_processing,
        mark_as_shipped,
        mark_as_delivered,
        mark_as_cancelled
    ]

    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = "User Email"

    def get_item_count(self, obj):
        return obj.items.count()
    get_item_count.short_description = "Items"

    def get_order_items_summary(self, obj):
        items = obj.items.all()
        if not items:
            return "No items in this order"

        html = '<table style="width:100%; border-collapse: collapse;">'
        html += '<tr style="background-color:#f0f0f0;border:1px solid #ddd;">'
        html += '<th style="padding:8px;border:1px solid #ddd;">Product</th>'
        html += '<th style="padding:8px;border:1px solid #ddd;">Price</th>'
        html += '<th style="padding:8px;border:1px solid #ddd;">Quantity</th>'
        html += '<th style="padding:8px;border:1px solid #ddd;">Subtotal</th></tr>'

        for item in items:
            html += f'''
            <tr style="border:1px solid #ddd;">
                <td style="padding:8px;border:1px solid #ddd;">{item.product_name}</td>
                <td style="padding:8px;border:1px solid #ddd;">Rs {item.price_at_purchase}</td>
                <td style="padding:8px;border:1px solid #ddd;">{item.quantity}</td>
                <td style="padding:8px;border:1px solid #ddd;">Rs {item.calculate_subtotal():.2f}</td>
            </tr>
            '''

        html += f'''
        <tr style="background-color:#f0f0f0;border:1px solid #ddd;font-weight:bold;">
            <td colspan="3" style="padding:8px;border:1px solid #ddd;">Total:</td>
            <td style="padding:8px;border:1px solid #ddd;">Rs {obj.calculate_total():.2f}</td>
        </tr>
        </table>
        '''

        return mark_safe(html)

    get_order_items_summary.short_description = "Order Items"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product_name', 'price_at_purchase', 'quantity', 'get_subtotal')
    list_filter = ('order__order_date', 'order__status')
    search_fields = ('product_name', 'order__id', 'order__user__email')
    readonly_fields = ('product_name', 'price_at_purchase', 'quantity', 'content_type', 'object_id')

    def get_subtotal(self, obj):
        return f"Rs {obj.calculate_subtotal():.2f}"
    get_subtotal.short_description = "Subtotal"


@admin.register(RefundRequest)
class RefundRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'user', 'status', 'created_at', 'get_reason_preview')
    list_filter = ('status', 'created_at')
    search_fields = ('order__id', 'user__email', 'reason')
    readonly_fields = ('order', 'user', 'reason', 'created_at')
    fields = ('order', 'user', 'reason', 'status', 'admin_note', 'created_at')
    actions = ['approve_refund', 'reject_refund']

    def get_reason_preview(self, obj):
        return obj.reason[:50] + '...' if len(obj.reason) > 50 else obj.reason
    get_reason_preview.short_description = "Reason"

    def approve_refund(self, request, queryset):
        for refund in queryset:
            if refund.status != 'approved':
                refund.status = 'approved'
                refund.save()
                order = refund.order
                order.status = 'refunded'
                order.track_order_status = 'Order cancel and refunded'
                order.save()
                payment = getattr(order, 'payment_record', None)
                if payment:
                    payment.status = 'refunded'
                    payment.save()
        self.message_user(request, f"{queryset.count()} refund(s) approved.")
    approve_refund.short_description = "✓ Approve refunds"

    def reject_refund(self, request, queryset):
        for refund in queryset:
            refund.status = 'rejected'
            refund.save()
        self.message_user(request, f"{queryset.count()} refund(s) rejected.")
    reject_refund.short_description = "✗ Reject refunds"