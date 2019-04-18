from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django import forms
from ..models import *
from .util_views import *

BC_FORM_FIELDS = ['name', 'members']


class BlockchainCreateView(LoginRequiredMixin, CreateView):
    """This view allows a user to create a new blockchain for which they are an admin. The user can input the name of
    the blockchain, as well as check off who they would like as members of the blockchain.
    This single CBV (class-based-view) handles the GET (which returns to the user the page on which they can input the
    blockchain information), as well as the POST (which receives the data submitted by the user, creates a new
    blockchain, and redirects the user to that blockchain's detail page).

    """
    model = Blockchain
    fields = BC_FORM_FIELDS
    template_name = "bcplatform/blockchain_create_update_form.html"

    def get_form(self, form_class=None):
        # Get the form displayed to the user, for manipulation
        form = super().get_form(form_class)
        # Change the widget to checkboxes, so it's easier
        form.fields['members'].widget = forms.CheckboxSelectMultiple()
        # Exclude the current user (the admin) from the list of members
        form.fields['members'].queryset = form.fields['members'].queryset.exclude(user=self.request.user)

        return form

    # Overridden to set the new blockchain's admin to the current user
    def form_valid(self, form):
        # Set the admin of the newly created blockchain instance to the current user.
        form.instance.admin = self.request.user.blockchainuser

        # Call super()... to validate the form as it is, and save the newly created Blockchain. We need to call this
        # here (as opposed to the end) because we can't create the genesis block for this blockchain until the
        # blockchain object itself is saved to the DB. We need to catch the response that is returned by this call, so
        # we can return it at the end.
        response = super().form_valid(form)

        # Create genesis block for the newly created blockchain, for all subsequent blocks to be chained to.
        form.instance.create_genesis_block()

        # Once the genesis block is created and the blockchain is saved to the DB already, return the response we
        # caught earlier.
        return response

    # This function returns the url that the user should be redirected to upon submitting the blockchain data.
    def get_success_url(self):
        # Redirect to the blockchain's detail view. the reverse() func, given a name and kwargs, returns an actual url.
        # The kwarg 'pk' means the primary key of the newly created blockchain, as the url for detailview needs this
        # parameter to know which blockchain to show the details for.
        return reverse("bcplatform:blockchain_detail_view", kwargs={'pk': self.object.pk})


class BlockchainUpdateView(OwnerRequiredMixin, LoginRequiredMixin, UpdateView):
    """This view, similar to the BlockchainCreateView, allows the user to update their blockchain info. This view uses
    the same exact HTML template as the above view, except that the form is prepopulated with the blockchain's previous
    information. This view also handles both the GET and the POST.
    """
    model = Blockchain
    fields = BC_FORM_FIELDS
    template_name = "bcplatform/blockchain_create_update_form.html"

    def get_form(self, form_class=None):
        # Get the form displayed to the user, for manipulation
        form = super().get_form(form_class)
        # Change the widget to checkboxes, so it's easier
        form.fields['members'].widget = forms.CheckboxSelectMultiple()
        # Exclude the current user (the admin) from the list of members
        form.fields['members'].queryset = form.fields['members'].queryset.exclude(user=self.request.user)

        return form

    def get_success_url(self):
        return reverse("bcplatform:blockchain_detail_view", kwargs={'pk': self.object.pk})


class BlockchainDetailView(OwnerOrMemberRequiredMixin, LoginRequiredMixin, DetailView):
    """This view handles showing the user the details of their blockchain, such as a list of their blockchain members,
    and a list of the blockchain's blocks.
    """
    model = Blockchain
    template_name = "bcplatform/blockchain_detail_view.html"
    context_object_name = "bc"

    # Adds extra data to the context, for use in the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bc_blocks = self.object.get_blocks()
        bc_members = self.object.get_members()
        bc_duplicates = self.object.duplicateblockchain_set.all()
        context['bc_blocks'] = bc_blocks
        context['bc_members'] = bc_members
        context['bc_duplicates'] = bc_duplicates
        return context


class BlockchainDeleteView(OwnerRequiredMixin, LoginRequiredMixin, DeleteView):
    """This view handles allowing the user to delete their blockchain. It handles the GET (which returns a page asking
    the user to confirm they would like to delete the blockchain), as well as the POST (in which the confirmation is
    received, the blockchain is deleted, and the user is redirected to their homepage).
    """
    model = Blockchain
    template_name = "bcplatform/blockchain_delete_form.html"
    success_url = reverse_lazy("bcplatform:homepage")
