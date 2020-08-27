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

    PLACE_RATING = [
        ("1", "One star"),
        ("2", "Two stars"),
        ("3", "Three stars"),
        ("4", "Four stars"),
        ("5", "Five stars"),
    ]

    name_of_place = models.CharField("Name of place", max_length=50,
                                     blank=False)
    type_of_place = models.CharField("Type of place", max_length=30,
                                     choices=TYPE_OF_PLACE, blank=False)
    place_description = models.CharField("Short description", max_length=500,
                                         blank=True)
    place_pic = models.ImageField(upload_to='public/media/',
                                  null=True, blank=True)
    location = models.CharField("The location of place", max_length=25,
                                choices=LOCATION, blank=False)
    rating = models.CharField("The rating of place", max_length=25,
                              choices=PLACE_RATING, blank=False)

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
