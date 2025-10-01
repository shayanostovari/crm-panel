from django.contrib.auth import get_user_model, login
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SignupSerializer, UserSerializer

User = get_user_model()

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer

class LoginView(APIView):
    def post(self, request):
        username_or_phone = request.data.get("username")
        password = request.data.get("password")

        user = User.objects.filter(username=username_or_phone).first() \
               or User.objects.filter(phone_number=username_or_phone).first()

        if user and user.check_password(password):
            login(request, user)  # سشن جنگو ایجاد می‌کنه
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
