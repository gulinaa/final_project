
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status
from .serializers import *
from .models import *


class PermissionMixin:

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'delete', 'destroy', 'create']:
            permissions= [IsAdminUser, ]

        elif self.action == 'favorite':
            permissions = [IsAuthenticated]
        else:
            permissions = []

        return [permission() for permission in permissions]


class GuesthouseViewSet(PermissionMixin, ModelViewSet):
    queryset = GuestHouse.objects.all()
    serializer_class = GuestHouseSerializer


class HotelViewSet(PermissionMixin,ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    @action(methods=['GET'], detail=False)
    def search(self, request):
        q = request.query_params.get('q')
        queryset = self.get_queryset().filter(
            Q(name__icontains=q)
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def recommendation(self, request):
        q = request.query_params.get('q')
        queryset = self.get_queryset().filter(
            Q(name__icontains=q)
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def favorites(self, request):
        queryset = Favorite.objects.all()
        queryset = queryset.filter(user=request.user)
        serializer = FavoriteSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        hotel = self.get_object()
        obj, created = Favorite.objects.get_or_create(user=request.user, hotel=hotel, )
        if not created:
            obj.favorite = not obj.favorite
            obj.save()

        favorites = 'added to favorites' if obj.favorite else 'discard favorites'

        return Response(f'Successfully {favorites}', status=status.HTTP_200_OK)

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ]


class LikesViewSet(ModelViewSet):
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer
    permission_classes = [IsAuthenticated, ]


class RatingViewSet(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated, ]
