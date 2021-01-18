from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreationForm
from django.contrib.auth.views import LoginView


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("login") #  где login — это параметр "name" в path()
    template_name = "regNew.html"
