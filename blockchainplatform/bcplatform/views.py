from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *

def get_blockchain_user(user):
    return BlockchainUser.objects.get(user=user)

# Create your views here.
class HomepageView(LoginRequiredMixin, TemplateView):
    template_name = "bcplatform/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        blockchain_user = get_blockchain_user(self.request.user)

        own_blockchains = blockchain_user.blockchains.all()
        other_blockchains = blockchain_user.other_blockchains.all()

        print(context)
        return context
