# Django modules.
from django.views import generic

# !Triplinker modules:

# Current app modules.
from accounts.forms.forms import ProfileEditForm
from accounts.models.TLAccount_frequest import TLAccount


class ProfileEditView(generic.FormView):
    """Gives the possibility of editing profile's data for current user."""
    model = TLAccount
    form_class = ProfileEditForm
    template_name = 'accounts/profile_edit.html'
    user = None
    success_url = '/profile/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'user'):
            kwargs.update({'instance': self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)
