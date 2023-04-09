from django.contrib import admin

from .models import Post, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'date_joined')
    list_display_links = ('username',)
    list_filter = ('is_active', 'is_superuser', 'is_staff')
    search_fields = ('id', 'username', 'email', 'date_joined')
    fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined',
              'last_login', 'is_superuser', 'is_active', 'is_staff')
    readonly_fields = ('id', 'last_login', 'date_joined', 'is_superuser')


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'pub_date')
    list_display_links = ('title',)
    search_fields = ('id', 'title', 'text', 'pub_date')
    fields = ('id', 'title', 'text', 'author', 'pub_date')
    readonly_fields = ('id', 'pub_date')


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
