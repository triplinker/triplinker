# Django modules.
from django.http import HttpResponseRedirect
from django.urls import reverse


def index_view(request):
    """Rederects to the page with feed"""
    return HttpResponseRedirect(reverse('accounts:feed'))
