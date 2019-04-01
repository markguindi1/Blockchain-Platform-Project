from django.core.exceptions import PermissionDenied


# Mixin for preventing user from editing a Blockchain for which they are not an admin
class OwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().admin != self.request.user.blockchainuser:
            raise PermissionDenied("You don't have authorization to view this page.")
        return super().dispatch(request, *args, **kwargs)
