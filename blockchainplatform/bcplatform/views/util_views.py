from django.core.exceptions import PermissionDenied


# Mixin for preventing user from editing a Blockchain for which they are not an admin
class OwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not self.is_admin(request, args, kwargs):
            raise PermissionDenied("You don't have authorization to view this page.")
        return super().dispatch(request, *args, **kwargs)

    def is_admin(self, request, *args, **kwargs):
        return self.get_object().admin == request.user.blockchainuser


# Mixin for preventing user from adding data to a Blockchain for which they are not an admin or member
class OwnerOrMemberRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if (not self.is_admin(request, args, kwargs)) and (not self.is_member(request, args, kwargs)):
            raise PermissionDenied("You don't have authorization to view this page.")
        return super().dispatch(request, *args, **kwargs)

    def is_admin(self, request, *args, **kwargs):
        return self.get_object().admin == request.user.blockchainuser

    def is_member(self, request, *args, **kwargs):
        return request.user.blockchainuser in self.get_object().get_members()
