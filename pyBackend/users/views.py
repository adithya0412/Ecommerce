from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer, UserRegistrationSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        user_data = UserSerializer(user).data
        
        return Response({
            'user': user_data,
            'token': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    
    # Check for duplicate email error
    if 'email' in serializer.errors:
        email_errors = serializer.errors['email']
        for error in email_errors:
            if 'already exists' in str(error) or 'unique' in str(error).lower():
                return Response({'message': 'User already exists with this email'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'message': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, email=email, password=password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        user_data = UserSerializer(user).data
        
        return Response({
            'user': user_data,
            'token': str(refresh.access_token),
        })
    
    return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'message': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, email=email, password=password)
    
    if user is not None and user.role == 'admin':
        refresh = RefreshToken.for_user(user)
        user_data = UserSerializer(user).data
        
        return Response({
            'user': user_data,
            'token': str(refresh.access_token),
        })
    
    return Response({'message': 'Invalid admin credentials'}, status=status.HTTP_401_UNAUTHORIZED)
