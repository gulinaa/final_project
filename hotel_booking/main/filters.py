from django_filters import rest_framework as filters
from hotel_booking.main.models import Hotel, GuestHouse


class HotelFilter(filters.FilterSet):
    price_from = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_to = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Hotel
        fields = ['room_type']


class HotelRatingFilter(filters.FilterSet):
    rating_from = filters.NumberFilter(field_name='rating', lookup_expr='gte')
    rating_to = filters.NumberFilter(field_name='rating', lookup_expr='lte')

    class Meta:
        model = GuestHouse
        fields = ['room_type']


# class HotelFilter(filters.FilterSet):
#     arrival_from = filters.NumberFilter(field_name='arrival_date', lookup_expr='gte')
#     departure_to = filters.NumberFilter(field_name='departure_date', lookup_expr='lte')
#
#     class Meta:
#         model = Room
#         fields = ['booking']


