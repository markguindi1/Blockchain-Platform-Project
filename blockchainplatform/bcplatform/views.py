from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *

# Create your views here.
class HomepageView(LoginRequiredMixin, TemplateView):
    template_name = "bcplatform/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        blockchainuser = self.request.user.blockchainuser

        own_blockchains = blockchainuser.blockchains.all()
        other_blockchains = blockchainuser.other_blockchains.all()

        context["own_blockchains"] = own_blockchains
        context["other_blockchains"] = other_blockchains
        return context
