from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import UserSerializer


class HelloView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        return Response(data={'message': f"Hello {request.user.username}!"})


class RegisterAPIView(CreateAPIView):

    serializer_class = UserSerializer



class LogoutAPIView(GenericAPIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request):
        request.user.auth_token.delete()
        return Response(data={'message': f"Bye {request.user.username}!"})