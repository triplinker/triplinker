from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from accounts.models.TLAccount_frequest import TLAccount
from .models import Journey
from .forms import AddJourneyForm, AddActivityForm


def activity_form_api(request):
    print(request.POST)
    form = AddActivityForm(request.POST)
    if form.is_valid():
        activity = form.save(commit=False)
        activity.journey = Journey.objects.get(id=request.POST['journey_id'])
        activity.save()
        context = {
            'status': True,
        }
        return JsonResponse(context, safe=False)
    return JsonResponse({'status': False}, safe=False)


def journey_form_api(request):
    form = AddJourneyForm(request.POST)
    if form.is_valid():
        journey = form.save(commit=False)
        journey.who_added_the_journey = request.user
        journey.save()
        journey.participants.add(request.user)
        journey.save()
        context = {
            'journey_id': journey.id,
            'status': True,
        }
        return JsonResponse(context, safe=False)
    return JsonResponse({'status': False}, safe=False)

from .helpers.views.get_allowed_journeys import get_allowed_journeys


def add_new_journey(request):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('journeys:journey-list',
                                    kwargs={'user_id': request.user.id}))
    context = {
        'form': AddJourneyForm(),
        'activity_form': AddActivityForm(),
    }

    if request.method == 'POST':
        form = AddJourneyForm(request.POST)

        if form.is_valid():
            final_form = form.save(commit=False)
            final_form.who_added_the_journey = request.user
            final_form.save()
            journ = Journey.objects.filter(who_added_the_journey=request.user)
            last_journey = journ.order_by('-timestamp').first()
            last_journey.particapants.add(request.user)

            return HttpResponseRedirect(
                           reverse('journeys:journey-list',
                                   kwargs={'user_id': request.user.id}))
        else:
            context['form'] = form
            return render(request, 'journeys/add_journey_form.html', context)
    # If HTTP method is GET...
    else:
        return render(request, 'journeys/add_journey_form.html', context)


def user_journey_list(request, user_id):
    current_user = request.user
    another_user = get_object_or_404(TLAccount, id=user_id)

    journeys = get_allowed_journeys(current_user, another_user)
    context = {
        'user_acc': another_user,
        'journeys': journeys
    }
    return render(request, 'journeys/user_journeys_list.html', context)


def journey_page(request, journey_id):
    journey = get_object_or_404(Journey, id=journey_id)
    creator_of_journeys_page = journey.who_added_the_journey
    context = {
        'journey': journey,
        'creator_of_journeys_page': creator_of_journeys_page,
    }
    return render(request, 'journeys/journey_page.html', context)


def sort_journeys_by_rating_of_place(request, user_id):
    user = get_object_or_404(TLAccount, id=user_id)
    journeys = Journey.objects.filter(particapants=user)
    sort = sorted(journeys,
                  key=lambda journey: journey.place.get_rating_of_place(),
                  reverse=False)

    context = {
        'user_acc': user,
        'journeys': sort,
    }
    return render(request, 'journeys/user_journeys_list.html', context)


def sort_journeys_by_date(request, user_id):
    user = get_object_or_404(TLAccount, id=user_id)
    jrnes = Journey.objects.filter(particapants=user).order_by("date_of_start")

    context = {
        'user_acc': user,
        'journeys': jrnes,
    }
    return render(request, 'journeys/user_journeys_list.html', context)
