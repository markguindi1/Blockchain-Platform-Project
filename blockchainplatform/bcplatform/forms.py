from django import forms
from . import models

# class BlockchainForm(ModelForm):
#     class Meta:
#         model = models.Blockchain
#         fields = ['name', 'members']

# class BlockCorruptionForm(Form):
#     pass


class BlockForm(forms.Form):
    data = forms.CharField(max_length=255, widget=forms.Textarea)


