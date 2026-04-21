from django.contrib import admin
from .models import BlogPost, BookingRequest


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
