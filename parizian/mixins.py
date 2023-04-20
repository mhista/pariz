from django.contrib.auth.mixins import AccessMixin, PermissionRequiredMixin
from django.shortcuts import redirect,reverse

class SuperUserRequired(AccessMixin):
    """Verify that the current user is authenticated."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser or not request.user.is_authenticated:
            return redirect(reverse('parizian:index'))
        return super().dispatch(request, *args, **kwargs)