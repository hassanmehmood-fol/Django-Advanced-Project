from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.models import Ingredient, User ,Recipe

class UserAdmin(BaseUserAdmin):
    # Fields to display in admin
    list_display = ('email', 'name', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'name')
    ordering = ('email',)

    # Fields for creating/editing users
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser'),
        }),
    )

admin.site.register(User, UserAdmin)



class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'time_minutes', 'price')  # Columns in list view
    list_filter = ('user', 'time_minutes')                     # Filters in sidebar
    search_fields = ('title', 'description', 'user__email')   # Search box
    ordering = ('title',)

admin.site.register(Recipe)
admin.site.register(Ingredient)

