from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
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


class BlockchainCreateView(LoginRequiredMixin, CreateView):
    model = Blockchain
    fields = ['name', 'members']
    template_name = "bcplatform/blockchain_create_form.html"
    # template_name_suffix = "_create_form"
    success_url = reverse_lazy("bcplatform:homepage")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['members'].queryset = BlockchainUser.objects.exclude(user=self.request.user)
        return form

    # Overridden to set the new blockchain's admin to the current user
    def form_valid(self, form):
        form.instance.admin = self.request.user.blockchainuser
        return super().form_valid(form)


class BlockchainDetailView(LoginRequiredMixin, DetailView):
    template_name = "bcplatform/blockchain_detail_view.html"
    model = Blockchain
    context_object_name = "bc"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bc_blocks = self.object.get_blocks()
        bc_members =  self.object.get_members()
        context['bc_blocks'] = bc_blocks
        context['bc_members'] = bc_members
        return context





