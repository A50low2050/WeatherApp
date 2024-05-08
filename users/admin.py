from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import UserCreationForm, UserChangeForm


@admin.register(User)
class AdminCustomerUser(UserAdmin):
    """ Admin for manage users """

    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ["id", "username"]

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            return self.add_form
        else:
            return super().get_form(request, obj, **kwargs)

    def get_fieldsets(self, request, obj=None):
        if obj:
            fieldsets = (
                ("User", {"fields": ("username", "password")}),
                ("Status", {"fields": ("is_superuser", "is_active", "is_staff")}),
                ("Permissions", {"fields": ("user_permissions", "groups")}),
                ("Activity", {"fields": ("last_login", "date_joined")}),

            )
            return fieldsets
        else:
            fieldsets = (
                ("User", {"fields": ("username", "password1", "password2")}),
            )
            return fieldsets

