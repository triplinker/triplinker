from django.views import generic  # noqa: F401
from django.http import HttpResponseRedirect
from django.urls import reverse

from accounts.models.TLAccount_frequest import TLAccount  # noqa: F401


def index_view(request):
    return HttpResponseRedirect(reverse('accounts:feed'))

# class IndexView(generic.ListView):
#     template_name = 'accounts/index.html'

#     def get_queryset(self):
#         return TLAccount.objects.all()
