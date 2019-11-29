from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TemporaryBanIP, ConfirmedUser
from .forms import ConfirmedUserChangeForm, ConfirmedUserCreationForm


@admin.register(TemporaryBanIP)
class TemporaryBanIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'status', 'attempts', 'time_unblock')
    search_fields = ('ip_address',)


class ConfirmedUserAdmin(UserAdmin):
    form = ConfirmedUserChangeForm
    add_form = ConfirmedUserCreationForm
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('confirm',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
            (None, {'fields': ('email',)}),
    )
    list_display = UserAdmin.list_display + ('confirm',)

admin.site.register(ConfirmedUser, ConfirmedUserAdmin)