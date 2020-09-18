def get_rating(journey) -> int:
    place_1_rating = journey.place_from.get_rating_of_place()
    place_2_rating = journey.place_to.get_rating_of_place()
    avg_rating = (place_1_rating + place_2_rating) / 2
    return avg_rating
