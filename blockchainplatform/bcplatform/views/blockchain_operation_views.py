from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from ..models import *
from .util_views import *

BLOCK_FORM_FIELDS = ['data']

class BlockCreateView(LoginRequiredMixin, CreateView):
    model = Block
    fields = BLOCK_FORM_FIELDS
    template_name = "bcplatform/blockchain_create_update_form.html"

    # Overridden to set the new blockchain's admin to the current user
    def form_valid(self, form):

        return super().form_valid(form)