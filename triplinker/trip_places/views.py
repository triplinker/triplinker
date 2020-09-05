from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404

from accounts.models.TLAccount_frequest import TLAccount
from feed.models import Post, Notification
from feed.forms import AddPostToPlacePageForm, AddCommentForm

from .models import Place
from .forms import (AddPlaceForm, AddPhotoToPlaceGalleryForm,
                    AddFeedbackForm)


def all_places(request):
    places = Place.objects.all()

    context = {
        'places': places,
    }
    return render(request, 'trip_places/all_places.html', context)


def favourite_places(request, user_id):
    places = Place.objects.filter(followers=user_id)

    context = {
        'places': places,
    }
    return render(request, 'trip_places/favourite_places.html', context)


def add_place(request):
    if request.method == 'POST':
        form = AddPlaceForm(request.POST, request.FILES)
        if form.is_valid():
            final_form = form.save(commit=False)
            final_form.who_added_place_on_site = request.user
            final_form.save()
            return HttpResponseRedirect(reverse('trip_places:all-places'))
        else:
            context = {
                'form': AddPlaceForm(request.POST, request.FILES)
            }
            return render(request, 'trip_places/add_place_form.html', context)

    else:
        form = AddPlaceForm()

        context = {
            'form': form
        }
        return render(request, 'trip_places/add_place_form.html', context)


def place_page(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    feed_of_place = Post.objects.filter(place=place, is_place=True)

    form = AddPostToPlacePageForm()
    comment_form = AddCommentForm()

    context = {
        'place': place,
        'feed_of_place': feed_of_place,
        'form': form,
        'comment_form': comment_form,
    }

    if request.method == 'POST':
        post_id = request.POST.get("post_id", )
        if post_id:
            # User adds a comment.
            content_for_comment_form = {
                'body': request.POST.get("body", ),
                'user': request.user,
                'post': post_id
            }
            comment_form = AddCommentForm(content_for_comment_form)
            context['comment_form'] = comment_form
            if comment_form.is_valid():
                comment_form.save()
                html_anchor = '#post-' + str(post_id) + "-content"
                return HttpResponseRedirect(
                       reverse('trip_places:place-page',
                               kwargs={'place_id': place_id}) + html_anchor)
            else:
                render(request, 'trip_places/feed/final_child_4.html', context)
        else:
            # User adds a post.
            form = AddPostToPlacePageForm(request.POST)
            if form.is_valid():
                final_form = form.save(commit=False)
                final_form.author = request.user
                final_form.place = place
                final_form.is_place = True
                final_form.save()
                postProfileLST = Post.objects.filter(place=place).first()
                html_anchor = '#post-' + str(postProfileLST.id) + "-content"
                return HttpResponseRedirect(
                       reverse('trip_places:place-page',
                               kwargs={'place_id': place_id}) + html_anchor)
            else:
                context['form'] = form
                comment_form = AddCommentForm()

                context['comment_form'] = comment_form
                return render(request, 'trip_places/feed/final_child_4.html',
                              context)

    # If HTTP method is GET...
    else:
        return render(request, 'trip_places/feed/final_child_4.html', context)


def edit_place_inf(request, place_id):
    place = Place.objects.get(id=place_id)

    if request.user.email != place.who_added_place_on_site.email:
        return HttpResponseNotFound()

    initial = {
        'name_of_place': place.name_of_place,
        'type_of_place': place.type_of_place,
        'place_description': place.place_description,
        'location': place.location
    }

    context = {
        'form': AddPlaceForm(initial=initial),
        'place_pic': place.place_pic
    }

    if request.method == 'POST':

        main_photo = request.FILES.get('place_pic', None)

        new_photo = False
        if main_photo:
            form = AddPlaceForm(request.POST,)
            new_photo = True
        else:
            form = AddPlaceForm(request.POST,)

        if form.is_valid():
            place.name_of_place = request.POST.get("name_of_place", None)
            place.type_of_place = request.POST.get("type_of_place", None)

            description = request.POST.get("place_description", None)
            place.place_description = description

            place.location = request.POST.get("location", None)

            if new_photo:
                place.place_pic = main_photo

            place.save()
            return HttpResponseRedirect(reverse('trip_places:place-page',
                                                args=(place_id, )))

        return render(request, 'trip_places/edit_place_form.html', context)
    else:
        return render(request, 'trip_places/edit_place_form.html', context)


# Photos of place
def photos_of_place(request, place_id):
    user_acc = get_object_or_404(TLAccount, id=request.user.id)
    place = get_object_or_404(Place, id=place_id)

    photos = place.photos_of_place.all()  # Custom related name

    context = {
        'place': place,
        'photos': photos
    }

    if request.method == 'POST':
        initial = {
            'place_pic': request.FILES['photo_with_current_place']
        }
        form = AddPhotoToPlaceGalleryForm(request.POST, initial)
        if form.is_valid():
            final_form = form.save(commit=False)
            final_form.place = place
            final_form.author = user_acc
            final_form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return render(request, 'trip_places/photos_gallery.html', context)

    # If HTTP method is GET...
    else:
        return render(request, 'trip_places/photos_gallery.html', context)


# Comments to place page
def comments_rating_page(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    author_of_feedback = get_object_or_404(TLAccount, id=request.user.id)
    feedbacks = place.place_feedback.all()
    context = {
        'form': AddFeedbackForm(),
        'place': place,
        'feedbacks': feedbacks,
    }

    if request.method == 'POST':
        form = AddFeedbackForm(request.POST)

        if form.is_valid():
            final_form = form.save(commit=False)
            final_form.place = place
            final_form.author = author_of_feedback
            final_form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            context['form'] = form
            return render(request, 'trip_places/rating_comments.html', context)

    # If HTTP method is GET...
    else:
        return render(request, 'trip_places/rating_comments.html', context)


# Favourite
def favourite_api(request, place_id):
    follow = False
    user = request.user

    ADD_PLACE_TEXT_POST = "Hey, I want to visit this place!"
    ADD_PLACE_TEXT_NOT = f"Your friend, {user}, add new favourite place"

    place = Place.objects.get(id=place_id)
    if user not in place.followers.all():
        place.followers.add(user)
        post = Post.objects.create(is_place=True, content=ADD_PLACE_TEXT_POST,
                                   author=user, place=place,
                                   notification_post=True)
        post.save()
        notification = Notification.objects.create(post=post,
                                                   text=ADD_PLACE_TEXT_NOT)
        notification.users.set(user.friends.all())
        notification.save()
        follow = True
    else:
        post = Post.objects.filter(author=user, is_place=True, place=place)
        post.delete()
        place.followers.remove(user)
        follow = False

    context = {
        'number_of_followers': place.number_of_followers(),
        'status': follow,
    }
    return JsonResponse(context, safe=False)
