from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .forms import UserCreationForm, UserChangeForm
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (_("User Important Info"), {
            "fields": (
                'email', 'first_name', 'last_name'
            ),
        }),
        (_("User Password"), {
            "fields": (
                'password',
            ),
        }),
        (_("User Permissions"), {
            "fields": (
                'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
            ),
        }),
        (_("Dates"), {
            "fields": (
                'last_login', 'date_joined'
            ),
        }),
    )

    add_fieldsets = (
        (_("Creating a None Staff User"), {
            "classes": (
                'wide',
            ),
            "fields": (
                'first_name', 'last_name','email',  'password1', 'password2', 'is_active',
            ),
        },),
    )

    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('last_name', 'email', 'is_superuser', 'is_staff', 'is_active', 'id')
    list_editable = ('is_active',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    readonly_fields = ('last_login',)
    search_fields = ('last_name', 'first_name', 'email')
    ordering = ('last_name',)
    list_per_page = 5
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            superuser_field = form.base_fields.get('is_superuser')
            if superuser_field:
                superuser_field.disabled = True
        return form

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request, queryset, search_term
        )
        try:
            search_term_as_int = int(search_term)
        except ValueError:
            pass
        else:
            queryset |= self.model.objects.filter(pk=search_term_as_int)

        return queryset, may_have_duplicates
