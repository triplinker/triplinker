from django.shortcuts import render, get_object_or_404

from accounts.models.TLAccount_frequest import TLAccount
from journeys.models import Journey

from .helpers.views.rating_getter import get_rating


def similar_jouneys(request):
    user = get_object_or_404(TLAccount, id=request.user.id)

    journeys_of_user_raw = Journey.objects.filter(particapants=user)

    final_dict = get_rating(user, journeys_of_user_raw)
    context = {
        'recommendations': final_dict
    }
    return render(request, 'recommendations/all_recommendations.html', context)
