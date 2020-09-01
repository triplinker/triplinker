def get_rating(place) -> float:
    all_feedbacks = place.place_feedback.all()

    if len(all_feedbacks) == 0:
        return 0

    rating_array = []
    for feedback in all_feedbacks:
        if feedback.rating.isdigit():
            rating_array.append(int(feedback.rating))

    accamulator = 0
    for num in rating_array:
        accamulator += num
    return round(accamulator / len(rating_array), 1)
