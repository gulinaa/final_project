from django.contrib.auth import get_user_model
from django.db import models

from hotel_booking.authentication.models import User

ROOM_TYPE = (
    ('STANDARD', 'standard'),
    ('PREMIUM', 'premium'),
    ('STUDIO ROOM', 'studio room'),
    ('EXECUTIVE SUITE', 'executive suite'),
    ('ROYAL', 'royal'),
    ('INTERCONNECTING ROOM', 'interconnecting room'),
    ('PENTHOUSE ROOM', 'penthouse room')
)
BED_TYPE = (
    ('TWIN', 'twin'),
    ('QUEEN', 'queen'),
    ('KING', 'king'),
    ('TRIPLE_BED', 'triple_bed')
)


class Hotel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    room_type = models.CharField(choices=ROOM_TYPE, max_length=100)
    bed_type = models.CharField(choices=BED_TYPE, max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name} {self.room_type} {self.bed_type} {self.price} {self.address}'


class HotelImage(models.Model):
    image = models.ImageField(upload_to='images')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='images')


class GuestHouse(models.Model):
    rooms = models.IntegerField(choices=((i, i) for i in range(1, 7)))
    description = models.TextField()
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='guesthouse')

    def __str__(self):
        return f'{self.hotel} {self.id}'


class GuestHouseImage(models.Model):
    image = models.ImageField(upload_to='images')
    villa = models.ForeignKey(GuestHouse, on_delete=models.CASCADE, related_name='images')


class Comment(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'{self.author}:{self.body}'


class Likes(models.Model):
    likes = models.BooleanField(default=False)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return str(self.likes)


RATING_CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10'),
)


class Rating(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rating')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating')
    text = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.rating)


class Favorite(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='favourites')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites')
    favorite = models.BooleanField(default=True)

