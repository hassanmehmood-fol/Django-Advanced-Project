from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from core.models import User
from .serializers import UserSerializer, LoginSerializer
from rest_framework import permissions



# Create new user
class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [] 


# Login + refresh API with JWT token
class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    permission_classes = []  # ← explicitly allow anyone to access login

    @swagger_auto_schema(request_body=LoginSerializer, 
    tags=['Login The User'],
    )
    
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh", None)

        # If refresh token is provided, generate new access token
        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                return Response({
                    "access": str(refresh.access_token)
                }, status=status.HTTP_200_OK)
            except TokenError:
                return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

        # Normal login flow
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Return access + refresh token along with user info
        return Response(
            serializer.to_representation(user),
            status=status.HTTP_200_OK
        )


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(
        tags=["Manage Users"],
        operation_description="Update the logged-in user's details"
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Manage Users"],
        operation_description="Partially update the logged-in user's details"
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


