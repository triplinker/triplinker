from datetime import date
from journeys.models import Journey


def get_rating(user, journeys_of_user_raw) -> dict:
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

    rating_of_recommendation = {}
    # Basis for recommendations.
    for journey_frnd in similar_journeys_of_friends:
        for journey_usr in journeys_of_user_clean:
            rating_var = 0
            if journey_usr.journey_from == journey_frnd.journey_from:
                rating_var += 1

            if journey_usr.journey_to == journey_frnd.journey_to:
                rating_var += 1

            if journey_usr.place == journey_frnd.place:
                rating_var += 1

            rating_of_recommendation[journey_frnd] = rating_var

    # Sorting by rating of recommendation.
    rec_rating = sorted(rating_of_recommendation,
                        key=lambda jrn: rating_of_recommendation[jrn],
                        reverse=True)

    final_dict = {}

    for journey in rec_rating:
        final_dict[journey] = rating_of_recommendation[journey]

    return final_dict
