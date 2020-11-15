from django.core.exceptions import PermissionDenied
from . models import AcceptedCreatorOrderModel

def dashboard_send_review_decorator(function):
    def wrap(request, *args, **kwargs):
        order = AcceptedCreatorOrderModel.objects.get(id=kwargs['id'])
        if order.creator == request.user:
            if order.stage == 'initial_stage':
                return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def dashboard_s_acc_decorator(function):
    def wrap(request, *args, **kwargs):
        order = AcceptedCreatorOrderModel.objects.get(id=kwargs['id'])
        if order.buyer  == request.user:
            if order.stage == 'review_content_sent':
                return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def dashboard_s_edit_decorator(function):
    def wrap(request, *args, **kwargs):
        order = AcceptedCreatorOrderModel.objects.get(id=kwargs['id'])
        if order.buyer  == request.user:
            if order.stage == 'review_content_sent':
                return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
