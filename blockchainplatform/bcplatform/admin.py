from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(BlockchainUser)
admin.site.register(Block)
admin.site.register(Blockchain)
admin.site.register(DuplicateBlockchain)
