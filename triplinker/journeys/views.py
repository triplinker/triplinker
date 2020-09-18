from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from accounts.models.TLAccount_frequest import TLAccount
from .models import Journey, Participant, Activity
from .forms import AddJourneyForm, AddActivityForm
from django.core.exceptions import PermissionDenied

from .helpers.views.get_allowed_journeys import get_allowed_journeys
from .helpers.views.get_average_rating import get_rating


def activity_form_api(request):
    form = AddActivityForm(request.POST)
    print(request.POST)
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
    print(request.POST)
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


def edit_journey(request, journey_id):

    journey = Journey.objects.get(pk=journey_id)

    if journey.who_added_the_journey != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = AddJourneyForm(request.POST, instance=journey)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('journeys:journey-page',
                                        kwargs={'journey_id': journey.id}))

    form = AddJourneyForm(instance=journey)
    return render(request, 'journeys/edit_journey.html', {'form': form})


def edit_activity(request, activity_id):

    activity = Activity.objects.get(pk=activity_id)

    if activity.journey.who_added_the_journey != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = AddActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('journeys:journey-page',
                                        kwargs={'journey_id':
                                                activity.journey.id}))

    form = AddActivityForm(instance=activity)
    return render(request, 'journeys/edit_activity.html', {'form': form})


def add_new_journey(request):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('journeys:journey-list',
                                    kwargs={'user_id': request.user.id}))
    context = {
        'form': AddJourneyForm(),
        'activity_form': AddActivityForm(),
    }
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
    journeys_raw = Participant.objects.filter(participant=user)

    journeys = []
    for participant_object in journeys_raw:
        journeys.append(participant_object.journey)

    sort = sorted(journeys, key=lambda journey: get_rating(journey),
                  reverse=False)

    context = {
        'user_acc': user,
        'journeys': sort,
    }
    return render(request, 'journeys/user_journeys_list.html', context)


def sort_journeys_by_date(request, user_id):
    user = get_object_or_404(TLAccount, id=user_id)
    journeys_raw = Participant.objects.filter(participant=user)

    journeys = []
    for participant_object in journeys_raw:
        journeys.append(participant_object.journey)

    sort = sorted(journeys, key=lambda journey: journey.date_of_start,
                  reverse=False)
    context = {
        'user_acc': user,
        'journeys': sort,
    }
    return render(request, 'journeys/user_journeys_list.html', context)


def join_journey(request, journey_id):
    journey = Journey.objects.get(pk=journey_id)
    journey.participants.add(request.user)
    journey.save()
    return HttpResponseRedirect(reverse('journeys:journey-page',
                                kwargs={'journey_id': journey_id}))


def leave_journey(request, journey_id):
    journey = Journey.objects.get(pk=journey_id)
    journey.participants.remove(request.user)
    journey.save()
    return HttpResponseRedirect(reverse('journeys:journey-page',
                                kwargs={'journey_id': journey_id}))
