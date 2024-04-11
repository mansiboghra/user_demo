from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import User


# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    filter_horizontal = ()
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        ('Personal info', {'fields': (
            'password', 'email', 'phone_number', 'name', 'image')}),
        ('Permissions',
         {'fields': ('is_active', 'is_staff', 'is_superuser')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}),
    )

    list_display = ['pk', 'email', 'phone_number']
    search_fields = ('email',)
    ordering = ('email',)



