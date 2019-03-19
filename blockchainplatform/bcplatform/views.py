from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class HomepageView(LoginRequiredMixin, TemplateView):
    template_name = "bcplatform/index.html"