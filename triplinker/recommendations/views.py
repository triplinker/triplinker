from django.shortcuts import render, get_object_or_404

from accounts.models.TLAccount_frequest import TLAccount
from journeys.models import Journey

from .helpers.views.recommendator import get_recommendations


def all_recommendations(request):
    user = get_object_or_404(TLAccount, id=request.user.id)

    journeys_of_user_raw = Journey.objects.filter(participants=user)

    # By default get_recommendations returns journeys and places.
    final_dict = get_recommendations(user, journeys_of_user_raw)
    context = {
        'recommendations': final_dict,
    }
    return render(request, 'recommendations/all_recommendations.html', context)


def jouneys_only(request):
    user = get_object_or_404(TLAccount, id=request.user.id)
    journeys_of_user_raw = Journey.objects.filter(participants=user)
    final_dict = get_recommendations(user, journeys_of_user_raw, type_r='J')
    context = {
        'recommendations': final_dict,
    }
    return render(request, 'recommendations/journeys_only.html', context)


def places_only(request):
    user = get_object_or_404(TLAccount, id=request.user.id)

    journeys_of_user_raw = Journey.objects.filter(participants=user)

    places_recommendations = get_recommendations(user, journeys_of_user_raw,
                                                 type_r="P")
    context = {
        'recommendations': places_recommendations
    }
    return render(request, 'recommendations/places_only.html', context)
