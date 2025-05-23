from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Donor, Foodbank, Recipient

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Custom Fields', {'fields': ('user_type',)}),
    )
    add_fieldsets = ( # Ensure add_fieldsets is also customized if creating users from admin
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_type', 'password', 'password2'), # password2 for confirmation
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, UserAdmin)
admin.site.register(Donor)
admin.site.register(Foodbank)
admin.site.register(Recipient)
