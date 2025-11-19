# accounts/views.py
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import SignupForm, LoginForm
from .models import CustomUser

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

# accounts/views.py → CORRIGÉ
class SignupView(CreateView):
    model = CustomUser
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:dashboard')  # ← AJOUTE accounts:

    def form_valid(self, form):
        user = form.save(commit=False)
        user.role = 'client'
        user.save()
        messages.success(self.request, "Inscription réussie ! Bienvenue !")
        return super().form_valid(form)

class ProfileView(UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name', 'email', 'phone', 'date_of_birth']
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')  # ← AJOUTE accounts:
    
    def get_object(self):
        return self.request.user

class DashboardView(TemplateView):
    template_name = 'accounts/dashboard.html'