from django.core.exceptions import PermissionDenied
from .models import BlogListingCreationModel

def user_is_entry_author(function):
    def wrap(request, *args, **kwargs):
        entry = BlogListingCreationModel.objects.get(id=kwargs['id'])
        if entry.creator == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
