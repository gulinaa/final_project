
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *

#
# class HiAuthView(generics.GenericAPIView):
#     def get(self, request):
#         return Response(data={"message": "Hi Auth"}, status=status.HTTP_200_OK)


class RegistrationView(APIView):
    def post(self, request):
        data = request.data
        from hotel_booking.authentication.serializers import RegistrationSerializer
        serializer = RegistrationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.create()
        return Response("You are successfully signed up!", status=201)


class ActivationView(APIView):
    def post(self, request):
        data = request.data
        from hotel_booking.authentication.serializers import ActivationSerializer
        serializer = ActivationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.activate()
        return Response("Your account successfully activated")


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.auth_token.delete()
        return Response('You are successfully logged out')


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = ChangePasswordSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.set_new_pass()
        return Response('Your password changed successfully')


class ForgotPasswordView(APIView):
    def post(self, request):
        data = request.data
        serializer = ForgotPasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.send_code()
        return Response('Confirmation code has been sent')


class ForgotPasswordCompleteView(APIView):
    def post(self, request):
        data = request.data
        serializer = ForgotPasswordCompleteSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_pass()
        return Response('You password has been reset successfully')


