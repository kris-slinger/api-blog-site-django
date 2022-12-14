from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import MyTokenObtainPairSerializer
from .models import CustomUser

from rest_framework_simplejwt.views import TokenObtainPairView

# for simplejwt authentication


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


"""
imprementation using session authentication
"""


@permission_classes([AllowAny])
@api_view(['POST'])
def loginView(request):
    username = request.data['username']
    password = request.data['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        if not request.user.is_authenticated:
            login(request, user)
            return Response({'msg': 'user successfully logged in'}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'already authenticated'}, status=status.HTTP_200_OK)
    return Response({"err": "unauthorised"}, status=status.HTTP_401_UNAUTHORIZED)


@permission_classes([AllowAny])
@api_view(['POST'])
def registerView(request):
    deserializer = RegisterSerializer(data=request.data)
    if deserializer.is_valid():
        userExist = CustomUser.objects.filter(
            username=deserializer.validated_data['username'])
        if not userExist:
            deserializer.save()
    else:
        return Response(deserializer.errors)
    return Response({"msg": "user created"})


@api_view(['GET'])
def logoutView(request):
    logout(request)
    return Response({"msg": "logged out successfully"}, status=status.HTTP_200_OK)
