from django.views import generic

from accounts.models.TLAccount_frequest import TLAccount


class IndexView(generic.ListView):
    template_name = 'accounts/index.html'

    def get_queryset(self):
        return TLAccount.objects.all()
