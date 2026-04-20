from django.contrib import admin
from .models import CustomerProfile


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display   = ('email', 'full_name', 'phone', 'city', 'state', 'verified')
    search_fields  = ('user__email', 'user__first_name', 'user__last_name', 'phone', 'city')
    list_filter    = ('state', 'user__is_active')
    raw_id_fields  = ('user',)
    readonly_fields = ('user',)

    def email(self, obj):
        return obj.user.email
    email.short_description = 'Email'
    email.admin_order_field = 'user__email'

    def full_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'.strip() or '—'
    full_name.short_description = 'Name'

    def verified(self, obj):
        return obj.user.is_active
    verified.boolean = True
    verified.short_description = 'Verified'
