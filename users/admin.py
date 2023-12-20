from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'gender', 'age', 'role', 'is_staff', 'is_active', 'email_confirmed')
    list_filter = ('gender', 'role', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'first_name','last_name', 'password', 'email_confirmed')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('gender', 'age', 'profile_image')}),
        ('Role', {'fields': ('role',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'gender', 'age', 'role', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'username',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
