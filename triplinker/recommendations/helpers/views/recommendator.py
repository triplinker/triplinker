# Python modules.
from datetime import date

# !Triplinker modules:

# Another apps modules.
from journeys.models import Journey
from trip_places.models import Place


def get_places_to_recommend(current_user, journeys_of_user_raw) -> list:
    journeys_of_user_clean = set()

    places_of_user = set()
    for journey in journeys_of_user_raw:
        journeys_of_user_clean.add(journey.place_from.location)
        journeys_of_user_clean.add(journey.place_to.location)
        places_of_user.add(journey.place_from)
        places_of_user.add(journey.place_to)

    countries_list_raw = Place._meta.get_field('location').choices

    countries_list_clean = set()
    for country in countries_list_raw:
        countries_list_clean.add(country[0])

    places_for_recommendation = set()
    for country in journeys_of_user_clean:
        all_places_of_country = Place.objects.filter(location=country)

        for place in all_places_of_country:
            if place in places_of_user:
                continue
            else:
                places_for_recommendation.add(place)
    return places_for_recommendation


def get_recommendations(user, journeys_of_user_raw, type_r='JP') -> dict:
    """ type_r
    J - means journeys,
    P - means places.
    If both are in type_r then the user will get all recommendations
    """
    rating_of_recommendation = {}
    if 'J' in type_r:
        current_time = date.today()
        journeys_of_user_clean = []

        for journey in journeys_of_user_raw:
            if journey.date_of_end > current_time:
                journeys_of_user_clean.append(journey)

        # Cleaning the journeys of user's friends.
        friends_of_user = user.friends.all()
        similar_journeys_of_friends = []

        for friend in friends_of_user:
            journeys_of_1_friend = Journey.objects.filter(participants=friend)

            for journey in journeys_of_1_friend:
                if (journey.date_of_end > current_time and
                   user not in journey.participants.all()):
                    similar_journeys_of_friends.append(journey)

        # Basis for recommendations.
        for journey_frnd in similar_journeys_of_friends:
            for journey_usr in journeys_of_user_clean:
                rating_var = 0

                if journey_usr.place_from == journey_frnd.place_from:
                    rating_var += 1

                if journey_usr.place_to == journey_frnd.place_to:
                    rating_var += 1

                if journey_usr.date_of_start == journey_frnd.date_of_start:
                    rating_var += 1

                if journey_usr.date_of_end == journey_frnd.date_of_end:
                    rating_var += 1

                rating_of_recommendation[journey_frnd] = rating_var

    if 'P' in type_r:
        places = get_places_to_recommend(user, journeys_of_user_raw)

        for place in places:
            rating_of_recommendation[place] = place.get_rating_of_place()

    # Sorting by rating of recommendation.
    rec_rating = sorted(rating_of_recommendation,
                        key=lambda jrn: rating_of_recommendation[jrn],
                        reverse=True)

    final_dict = {}

    for rec in rec_rating:
        final_dict[rec] = rating_of_recommendation[rec]

    return final_dict
