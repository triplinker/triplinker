from django.db.models import Q  # noqa: F401

from django.views import generic  # noqa: F401
from django.shortcuts import render

from accounts.models.TLAccount_frequest import UserFilter
from accounts.models.TLAccount_frequest import TLAccount


def all_users_list(request):
    f = UserFilter(request.GET, queryset=TLAccount.objects.all())
    return render(request, 'accounts/all_users_list.html', {'filter': f})
    