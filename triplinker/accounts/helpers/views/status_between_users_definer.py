def define_status(FriendRequest, current_user: int, 
    another_user: int) -> str:
    frequest_case_1 = FriendRequest.objects.filter(
        from_user= current_user, to_user=another_user)

    frequest_case_2 = FriendRequest.objects.filter(
        from_user= another_user, to_user=current_user)

    we_wanna_be_friends_with_user = bool(frequest_case_1)
    user_wanna_be_friends_with_us = bool(frequest_case_2)
    
    status_between_users = None

    if (we_wanna_be_friends_with_user == False and
        user_wanna_be_friends_with_us == True):
        return "User wanna be our friend"
    elif (we_wanna_be_friends_with_user == True and
        user_wanna_be_friends_with_us == False):
        return "We're waiting for user confirmation"
    elif (current_user in another_user.friends.all() and
        another_user in current_user.friends.all()):
        print("Friends")
        return "Friends"
    print(current_user.friends.all())
    return "Not friends"