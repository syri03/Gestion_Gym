# accounts/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'role_badge', 'phone', 'is_active_status', 'date_joined']
    list_filter = ['role', 'is_active', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name', 'phone']
    readonly_fields = ['date_joined', 'last_login']
    ordering = ['-date_joined']

    fieldsets = (
        ("Informations principales", {
            'fields': ('email', 'first_name', 'last_name', 'phone', 'date_of_birth')
        }),
        ("Rôle & Statut", {
            'fields': ('role', 'is_active', 'is_staff')
        }),
        ("Dates", {
            'fields': ('date_joined', 'last_login'),
            'classes': ('collapse',)
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone', 'role', 'password1', 'password2'),
        }),
    )

    # Badges personnalisés
    def role_badge(self, obj):
        color = "admin" if obj.role == "admin" else "client"
        return format_html(f'<span class="role-{color}">{obj.get_role_display()}</span>')
    role_badge.short_description = "Rôle"

    def is_active_status(self, obj):
        status = "active" if obj.is_active else "inactive"
        return format_html(f'<span class="status-{status}">{ "Actif" if obj.is_active else "Inactif" }</span>')
    is_active_status.short_description = "Statut"

    # Action : désactiver plusieurs comptes en une fois
    actions = ['deactivate_users', 'activate_users']

    def deactivate_users(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"{count} compte(s) désactivé(s).")
    deactivate_users.short_description = "Désactiver les comptes sélectionnés"

    def activate_users(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f"{count} compte(s) réactivé(s).")
    activate_users.short_description = "Réactiver les comptes sélectionnés"