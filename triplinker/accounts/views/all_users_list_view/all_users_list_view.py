# Django modules.
from django.shortcuts import render

# !Triplinker modules:

# Current app modules.
from accounts.models.TLAccount_frequest import TLAccount, UserFilter


def all_users_list(request):
    """Shows the list of all user (excluding current user)."""
    f = UserFilter(request.GET, queryset=TLAccount.objects.all())
    return render(request, 'accounts/all_users_list.html', {'filter': f})
