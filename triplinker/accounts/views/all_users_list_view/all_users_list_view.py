from django.db.models import Q

from django.views import generic
from django.shortcuts import render

from accounts.models.TLAccount_frequest import UserFilter
from accounts.models.TLAccount_frequest import TLAccount


# class AllUsersList(generic.ListView):
#     """Renders the list of users of site without the user who makes this
#     request."""
#
#     template_name = 'accounts/all_users_list.html'
#     context_object_name = 'users'
#
#     def get_queryset(self):
#         """Forms query set that will be used in the context of django template.
#         """
#         query = self.request.GET.get('q')
#         if query is None:
#             query = ''
#         users_list = TLAccount.objects.filter(
#             Q(first_name__icontains=query) |
#             Q(second_name__icontains=query) |
#             Q(email__icontains=query)
#         ).exclude(id=self.request.user.id)
#         return users_list

def all_users_list(request):
    f = UserFilter(request.GET, queryset=TLAccount.objects.all())
    return render(request, 'accounts/all_users_list.html', {'filter': f})
