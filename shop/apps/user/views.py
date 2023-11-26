from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import Throttled
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterUserSerializer
from .throttle import UserLoginRateThrottle


class UserCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerializer
    throttle_classes = (UserLoginRateThrottle,)

    # def perform_create(self, serializer):
    #     user = serializer.save()

    def throttled(self, request, wait):
        raise Throttled(detail={
            'message': "reCAPTCHA required"
        })


class BlackListTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)
