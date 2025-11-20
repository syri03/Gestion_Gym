# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin   # ← AJOUTÉ
from django.utils.html import format_html
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):                 # ← CHANGÉ ModelAdmin → UserAdmin
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

    # ← AJOUTE ÇA (3 lignes seulement)
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    # Le reste reste 100 % identique
    def role_badge(self, obj):
        color = "admin" if obj.role == "admin" else "client"
        return format_html(f'<span class="role-{color}">{obj.get_role_display()}</span>')
    role_badge.short_description = "Rôle"

    def is_active_status(self, obj):
        status = "active" if obj.is_active else "inactive"
        return format_html(f'<span class="status-{status}">{ "Actif" if obj.is_active else "Inactif" }</span>')
    is_active_status.short_description = "Statut"

    actions = ['deactivate_users', 'activate_users']
    def deactivate_users(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"{count} compte(s) désactivé(s).")
    deactivate_users.short_description = "Désactiver les comptes sélectionnés"

    def activate_users(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f"{count} compte(s) réactivé(s).")
    activate_users.short_description = "Réactiver les comptes sélectionnés"