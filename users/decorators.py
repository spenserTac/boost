from django.core.exceptions import PermissionDenied
from . models import AcceptedCreatorOrderModel, CreatorOrderModel, SponsorOrderModel, Profile, Messages
from django.contrib.auth.models import User


def dashboard_message_decorator(function):
    def wrap(request, *args, **kwargs):
        #id is id of message
        message = Messages.objects.get(id=kwargs['id'])
        if request.user == message.reciever:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def dashboard_edit_profile_decorator(function):
    def wrap(request, *args, **kwargs):
        user = User.objects.get(id=kwargs['id'])
        profile = Profile.objects.get(user=user)
        if profile.user == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def dashboard_send_review_decorator(function):
    def wrap(request, *args, **kwargs):
        order = AcceptedCreatorOrderModel.objects.get(id=kwargs['id'])
        if order.creator == request.user:
            if order.stage == 'initial_stage' or order.stage == 'sponsor_edits_sent':
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


def dashboard_c_next_step_decorator(function):
    def wrap(request, *args, **kwargs):
        order = AcceptedCreatorOrderModel.objects.get(id=kwargs['id'])
        if order.creator  == request.user:
            if order.stage == 'just_accepted':
                return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def dashboard_user_is_buyer(function):
    def wrap(request, *args, **kwargs):
        order = SponsorOrderModel.objects.get(id=kwargs['id'])
        try:
            order2 = AcceptedCreatorOrderModel.objects.get(id=kwargs['id'])
        except:
            order2 = None

        if order.creator == request.user or order2.buyer == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def dashboard_user_is_creator(function):
    def wrap(request, *args, **kwargs):
        order = CreatorOrderModel.objects.get(id=kwargs['id'])
        try:
            order2 = AcceptedCreatorOrderModel.objects.get(id=kwargs['id'])
        except:
            order2 = None

        if order.creator == request.user or order2.creator == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
