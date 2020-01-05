from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TemporaryBanIP, ConfirmedUser, CustomConfirmedUser
from .forms import ConfirmedUserChangeForm, ConfirmedUserCreationForm, \
    ConfirmedUserCreationForm, CustomConfirmedUserChangeForm


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


class CustomConfirmedUserAdmin(UserAdmin):
    form = ConfirmedUserCreationForm
    add_form = CustomConfirmedUserChangeForm
    fieldsets = (
        (None, {
            'fields': (
                'username',
                'email',
                'password',
                'confirm'
            ),
        }),
        ('Permissions', {
            'fields': (
                'is_active', 
                'is_staff', 
                'is_superuser', 
                'groups', 
                'user_permissions'
            )
        })
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'password1',
                'password2'
            )
        }),
    )
    readonly_fields = ('confirm',)
    list_display = ('username', 'email')

admin.site.register(CustomConfirmedUser, CustomConfirmedUserAdmin)