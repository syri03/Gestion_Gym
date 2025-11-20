# accounts/views.py
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash  # ← AJOUT OBLIGATOIRE
from django.contrib.auth.forms import SetPasswordForm          # ← déjà là

from .forms import SignupForm, LoginForm
from .models import CustomUser


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm


class SignupView(CreateView):
    model = CustomUser
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:dashboard')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.role = 'client'
        user.save()
        messages.success(self.request, "Inscription réussie ! Bienvenue !")
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name', 'email', 'phone', 'date_of_birth']
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_form'] = SetPasswordForm(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        # Gestion du changement de mot de passe
        if 'new_password1' in request.POST:
            password_form = SetPasswordForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)  # ← ne déconnecte pas l'utilisateur
                messages.success(request, "Mot de passe changé avec succès !")
                return self.get(request, *args, **kwargs)  # recharge la page proprement
            else:
                messages.error(request, "Erreur : mot de passe invalide ou non identique.")
        # Sinon, on traite le formulaire du profil normalement
        return super().post(request, *args, **kwargs)


class DashboardView(TemplateView):
    template_name = 'accounts/dashboard.html'