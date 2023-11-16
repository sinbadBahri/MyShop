from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'is_superuser', 'is_staff', 'is_active']
    list_editable = ['is_active']
    list_filter = ['is_superuser', "is_active"]
    search_fields = ['email', 'first_name', 'last_name']
    list_per_page = 5

# @admin.register(User)
# class MyUserAdmin(UserAdmin):
#     fieldsets = (
#         (_("User Important Info"), {
#             "fields": (
#                 'email', 'password'
#             ),
#         }),
#         (_("User Full Name"), {
#             "fields": (
#                 'first_name', 'last_name'
#             ),
#         }),
#         (_("User Permissions"), {
#             "fields": (
#                 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
#             ),
#         }),
#         (_("Dates"), {
#             "fields": (
#                 'last_login', 'date_joined'
#             ),
#         }),
#     )
#
#     add_fieldsets = (
#         (_("Ya Aliii"), {
#             "classes": (
#                 'wide',
#             ),
#             "fields": (
#                 'email', 'first_name', 'last_name', 'password1', 'password2'
#             ),
#         }),
#     )
#
#     list_display = ('email', 'is_staff', 'date_joined')
#     search_fields = ('email__exact',)
#     ordering = ('-id',)
#
#     def get_search_results(self, request, queryset, search_term):
#         queryset, may_have_duplicates = super().get_search_results(
#             request, queryset, search_term
#         )
#         try:
#             search_term_as_int = int(search_term)
#         except ValueError:
#             pass
#         else:
#             queryset |= self.model.objects.filter(pk=search_term_as_int)
#
#         return queryset, may_have_duplicates
#
#
# admin.site.unregister(Group)
