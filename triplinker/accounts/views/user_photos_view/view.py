from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from accounts.forms.forms import AddPhotoToPlaceGalleryForm
from accounts.models.TLAccount_frequest import TLAccount


def photos_of_user(request, user_id):
    template = 'accounts/profile/photos_gallery.html'
    user_acc = get_object_or_404(TLAccount, id=user_id)

    photos = user_acc.photos_of_user.all()  # Custom related name

    context = {
        'photos': photos,
        'user_acc': user_acc
    }

    if request.method == 'POST':

        if request.user.email != user_acc.email:
            return HttpResponseBadRequest()

        initial = {
            'photo': request.FILES['user_gallery_photo']
        }
        form = AddPhotoToPlaceGalleryForm(request.POST, initial)
        if form.is_valid():
            final_form = form.save(commit=False)
            # final_form.place = place
            final_form.author = user_acc
            final_form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return render(request, template, context)

    # If HTTP method is GET...
    else:
        return render(request, template, context)
