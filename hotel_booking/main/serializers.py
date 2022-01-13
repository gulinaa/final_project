
from rest_framework import serializers
from django.db.models import Avg
from .models import *


class GuestHouseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestHouse
        fields = ('image',)

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            return url
        return ''

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation


class GuestHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestHouse
        fields = '__all__'


    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        guesthouse = GuestHouse.objects.create(**validated_data)
        for image in images_data.getlist('images'):
            GuestHouse.objects.create(image=image, guesthouse=guesthouse)
        return guesthouse

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        images_data = request.FILES
        instance.images.all().delete()
        for image in images_data.getlist('images'):
            GuestHouse.objects.create(image=image, guesthouse=instance)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = GuestHouseImageSerializer(instance.images.all(), many=True).data
        return representation


class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ('image',)

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            return url
        return ''

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        comment = Comment.objects.create(author=request.user, **validated_data)
        return comment


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        hotel = Hotel.objects.create(**validated_data)
        for image in images_data.getlist('images'):
            HotelImage.objects.create(image=image, hotel=hotel)
        return hotel

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        images_data = request.FILES
        instance.images.all().delete()
        for image in images_data.getlist('images'):
            HotelImage.objects.create(image=image, hotel=instance)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = HotelImageSerializer(instance.images.all(), many=True).data
        representation['hostel'] = GuestHouseSerializer(instance.apartments.all(), many=True).data
        representation['comments'] = CommentSerializer(instance.comments.all(),
                                                       many=True).data
        representation['likes'] = instance.likes.all().count()
        representation['rating'] = instance.rating.aggregate(Avg('rating')).get("rating_avg")
        return representation


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email
        representation['hotel'] = instance.hotel.name
        return representation


class LikesSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Likes
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        hotel = validated_data.get('hotel')
        like = Likes.objects.get_or_create(author=author, hotel=hotel)[0]
        like.likes = True if like.likes is False else False
        like.save()
        return like


class RatingSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Rating
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        hotel = validated_data.get('hotel')
        print(validated_data)
        rating = Rating.objects.get_or_create(author=author, hotel=hotel)[0]
        rating.rating = validated_data['rating']
        print(rating)
        rating.save()
        return rating








