from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User
from user.serializers import UserLoginSerializer, Authenticate, UserCreateSerializer


# Create your views here.


class UserRegisterView(generics.CreateAPIView):
    """Register API View"""
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        response_data = dict()
        response_data['id'] = data.get('id')
        response_data['token'] = data.get('token')
        response_data['message'] = [
            'Successfully registered, please check inbox or spam folder for verify your email address.']
        return Response(response_data, status=status.HTTP_200_OK)


class UserLoginView(APIView):
    """This view endpoint for Ownerlogin"""
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        print(serializer.data.get("email"), '>>>.email')
        user = User.objects.get(email__iexact=serializer.data.get("email"))
        data = Authenticate(user, context={"request": self.request}).data  # This serializer presenting user data
        return Response(data, status=status.HTTP_200_OK)
