from django.contrib import admin
from .models import BlogPost, BookingRequest, GiftCard


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display        = ('title', 'published', 'is_live')
    list_filter         = ('is_live',)
    search_fields       = ('title', 'excerpt', 'body')
    prepopulated_fields = {'slug': ('title',)}
    list_editable       = ('is_live',)
    date_hierarchy      = 'published'


@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display  = ('first_name', 'last_name', 'email', 'phone', 'service_requested', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter   = ('created_at',)
    readonly_fields = ('created_at', 'ip_address')


@admin.register(GiftCard)
class GiftCardAdmin(admin.ModelAdmin):
    list_display    = ('code', 'amount', 'balance', 'recipient_name', 'recipient_email', 'is_active', 'redeemed_at', 'created_at')
    list_filter     = ('is_active',)
    search_fields   = ('code', 'recipient_email', 'buyer_email', 'recipient_name', 'buyer_name')
    readonly_fields = ('code', 'stripe_session_id', 'created_at')
    actions         = ['mark_fully_redeemed']

    def mark_fully_redeemed(self, request, queryset):
        from django.utils import timezone
        queryset.update(balance=0, redeemed_at=timezone.now())
    mark_fully_redeemed.short_description = 'Mark selected cards as fully redeemed'
