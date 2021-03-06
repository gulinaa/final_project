from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Message
from hotel_booking.authentication.models import User
from hotel_booking.bookings.serializer import UserSerializer, MessageSerializer


# class HiBookingsView(generics.GenericAPIView):
#     def get(self, request):
#         return Response(data={"message": "Hyyyyy Bookings"}, status=status.HTTP_200_OK)


@api_view(["GET", ])
def user_list(request, pk=None):

    if request.method == 'GET':
        if pk:
            users = User.objects.filter(id=pk)

        else:
            users = User.objects.all()

        serializer = UserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data, )


@api_view(["POST", "GET"])
def message_list(request):

    if request.method == 'GET':
        sender = request.user
        messages = Message.objects.filter(Q(sender_id=sender, ) | Q (receiver_id=sender,))
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return Response(serializer.data, )

    elif request.method == 'POST':
        data = request.data
        serializer = MessageSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

