from django.shortcuts import render
from django.views.generic import *


# Create your views here.
class HomepageView(TemplateView):
    template_name = "bcplatform/index.html"