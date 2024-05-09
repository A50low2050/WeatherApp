from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import UserCreationForm, UserChangeForm


@admin.register(User)
class UserManagement(UserAdmin):
    """ Admin for manage users """

    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ["id", "username", "date_joined"]
    readonly_fields = ["last_login", "date_joined"]

    def get_form(self, request, obj=None, **kwargs):
        disable_fields = (
            "is_superuser",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
        )

        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            for fields in disable_fields:
                if fields in form.base_fields:
                    form.base_fields[fields].disabled = True
            return form
        if obj is None:
            return self.add_form
        else:
            return super().get_form(request, obj, **kwargs)

    def get_fieldsets(self, request, obj=None):
        is_superuser = request.user.is_superuser

        if obj and is_superuser:
            fieldsets = (
                ("User", {"fields": ("username", "password")}),
                ("Status", {"fields": ("is_superuser", "is_active", "is_staff")}),
                ("Permissions", {"fields": ("user_permissions", "groups")}),
                ("Activity", {"fields": ("last_login", "date_joined")}),

            )
            return fieldsets
        if obj and not is_superuser:
            fieldsets = (
                ("User", {"fields": ("username", "password")}),
                ("Activity", {"fields": ("last_login", "date_joined")}),

            )
            return fieldsets

        else:
            fieldsets = (
                ("User", {"fields": ("username", "password1", "password2")}),
            )
            return fieldsets
