from django.forms import ModelForm
from . import models

class BlockchainForm(ModelForm):
    class Meta:
        model = models.Blockchain
        fields = ['name', 'members']
