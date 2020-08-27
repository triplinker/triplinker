from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from feed.models import Post
from feed.forms import AddPostToPlacePageForm, AddCommentForm

from .models import Place
from .forms import AddPlaceForm


def all_places(request):
    places = Place.objects.all()

    context = {
        'places': places,
    }
    return render(request, 'trip_places/all_places.html', context)


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
        'comment_form': comment_form
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
