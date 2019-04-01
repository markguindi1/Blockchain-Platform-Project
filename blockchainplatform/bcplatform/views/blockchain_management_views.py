from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from ..models import *
from .util_views import *

BC_FORM_FIELDS = ['name', 'members']


class BlockchainCreateView(LoginRequiredMixin, CreateView):
    model = Blockchain
    fields = BC_FORM_FIELDS
    template_name = "bcplatform/blockchain_create_update_form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        print(form.fields['members'].queryset)
        form.fields['members'].queryset = form.fields['members'].queryset.exclude(user=self.request.user)
        return form

    # Overridden to set the new blockchain's admin to the current user
    def form_valid(self, form):
        form.instance.admin = self.request.user.blockchainuser
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("bcplatform:blockchain_detail_view", kwargs={'pk': self.object.pk})


class BlockchainUpdateView(OwnerRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Blockchain
    fields = BC_FORM_FIELDS
    template_name = "bcplatform/blockchain_create_update_form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['members'].queryset = form.fields['members'].queryset.exclude(user=self.request.user)
        return form

    def get_success_url(self):
        return reverse("bcplatform:blockchain_detail_view", kwargs={'pk': self.object.pk})


class BlockchainDetailView(LoginRequiredMixin, DetailView):
    model = Blockchain
    template_name = "bcplatform/blockchain_detail_view.html"
    context_object_name = "bc"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bc_blocks = self.object.get_blocks()
        bc_members = self.object.get_members()
        context['bc_blocks'] = bc_blocks
        context['bc_members'] = bc_members
        return context


class BlockchainDeleteView(OwnerRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Blockchain
    template_name = "bcplatform/blockchain_delete_form.html"
    success_url = reverse_lazy("bcplatform:homepage")
