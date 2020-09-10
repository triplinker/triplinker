from journeys.models import Journey


def get_allowed_journeys(current_user, another_user) -> list:
    all_journeys_of_user = Journey.objects.filter(participants=another_user)
    permitted_journeys = []
    if current_user.email != another_user.email:
        for journey in all_journeys_of_user:
            if current_user not in journey.participants.all():
                visibility_of_journey = journey.get_visibility()
                if visibility_of_journey == 'FriendsFollowers':
                    if (current_user in another_user.friends.all() or
                       current_user in another_user.followers.all()):
                       permitted_journeys.append(journey)

                elif visibility_of_journey == 'Friends':
                    if current_user in another_user.friends.all():
                        permitted_journeys.append(journey)

                elif visibility_of_journey == 'Me':
                    continue
                else:
                    permitted_journeys.append(journey)
        return permitted_journeys
    else:
        return all_journeys_of_user

