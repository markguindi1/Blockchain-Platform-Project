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

