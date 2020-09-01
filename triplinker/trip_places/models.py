from django.db import models

from accounts.models.TLAccount_frequest import TLAccount


class Place(models.Model):
    TYPE_OF_PLACE = [
        ("TownCity", "Town or city"),
        ("NatureObj", "Object of nature"),
    ]

    LOCATION = [
        ("BY", "Belarus")
    ]

    name_of_place = models.CharField("Name of place", max_length=50,
                                     blank=False)
    type_of_place = models.CharField("Type of place", max_length=30,
                                     choices=TYPE_OF_PLACE, blank=False)
    place_description = models.CharField("Short description", max_length=500,
                                         blank=True)
    place_pic = models.ImageField('Main picture of the place',
                                  upload_to='places/main_pic',
                                  null=True, blank=True)
    location = models.CharField("The location of place", max_length=25,
                                choices=LOCATION, blank=False)

    related_name = 'user_who_added_place_on_site'  # For the field below.
    who_added_place_on_site = models.ForeignKey(TLAccount,
                                                related_name=related_name,
                                                blank=True, null=True,
                                                default=None,
                                                on_delete=models.CASCADE)
    followers = models.ManyToManyField(TLAccount,
                                       related_name='favourite_places',
                                       blank=True, default=None)

    def __str__(self):
        return self.name_of_place

    def get_full_value_type_of_place(self):
        """Returns full value in tuples of CHOICES"""
        return self.get_type_of_place_display()

    def get_full_value_location_of_place(self):
        """Returns full value in tuples of CHOICES"""
        return self.get_location_display()

    def number_of_followers(self):
        """Returns number of followers"""
        return self.followers.all().count()

    class Meta:
        app_label = 'trip_places'
        verbose_name = 'Place'
        verbose_name_plural = 'Places'


class Photo(models.Model):
    place = models.ForeignKey('Place', related_name='photos_of_place',
                              blank=True, null=True,
                              default=None,
                              on_delete=models.CASCADE)
    place_pic = models.ImageField('Photos of place',
                                  upload_to='places/photos_of_place',
                                  null=True, blank=True)

    author = models.ForeignKey(TLAccount, related_name='author_of_photo',
                               blank=True, null=True, default=None,
                               on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "Place: {}, Author: {}, Photo: {}".format(self.place,
                                                         self.author,
                                                         self.place_pic)

    class Meta:
        ordering = ('-timestamp',)
        app_label = 'trip_places'
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'


class Feedback(models.Model):
    PLACE_RATING = [
        ("no", "Without any assessment"),
        ("1", "★"),
        ("2", "★★"),
        ("3", "★★★"),
        ("4", "★★★★"),
        ("5", "★★★★★"),
    ]

    rating = models.CharField("The rating of place", max_length=25,
                              choices=PLACE_RATING, blank=False,)
    comment = models.TextField()
    author = models.ForeignKey(TLAccount, related_name='author_feedback',
                               on_delete=models.CASCADE, blank=True, null=True)
    place = models.ForeignKey('Place', related_name='place_feedback',
                              on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Author: {}, Rating: {}, Comment: {}".format(self.author,
                                                            self.rating,
                                                            self.comment)

    def get_rating_to_place_from_user(self):
        if self.rating == "no":
            return "No assessment"
        elif self.rating == "1":
            return "★"
        elif self.rating == "2":
            return "★★"
        elif self.rating == "3":
            return "★★★"
        elif self.rating == "4":
            return "★★★★"
        else:
            return "★★★★★"

    class Meta:
        ordering = ('-timestamp',)
        app_label = 'trip_places'
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'
