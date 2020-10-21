# Python modules.
import os

# Django modules.
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render

# !Triplinker modules:

# Current app modules.
from accounts.forms.forms import SetAvatarForm
from accounts.models.TLAccount_frequest import TLAccount


@require_http_methods(["GET", "POST"])
def set_avatar_view(request):
    """Displaying the page of changing an avatar and setting an avatar view."""
    usr = TLAccount.objects.get(id=request.user.id)

    if request.method == 'POST':
        get_avatar = usr.get_avatar.all()

        if len(get_avatar) == 1:
            particular_avatar = get_avatar.first()
            # Delete from filestorage.
            full_path = 'public' + particular_avatar.profile_image.url
            os.remove(full_path)

            # Delete from DB.
            particular_avatar.delete()

        form = SetAvatarForm(request.POST, request.FILES)
        if form.is_valid():
            final_form = form.save(commit=False)
            final_form.user = usr
            final_form.save()
            return HttpResponseRedirect(reverse('accounts:profile'))
        else:
            return HttpResponseBadRequest()
    # HTTP method is GET
    else:
        user_acc = TLAccount.objects.get(id=request.user.id)

        user_avatar = None
        try:
            user_avatar = user_acc.get_avatar.all().first()
        except Exception:
            pass

        form = SetAvatarForm()
        context = {'form': form, 'avatar': user_avatar}
        return render(request, 'accounts/profile/set_avatar_page.html',
                      context)
