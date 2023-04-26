from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated


from . import serializers
from . import models
from . import permissions

class MainApiViewSet(viewsets.ViewSet):
     """Test API View"""
     
     def list(self, request, pk=None):
         ex_viewset = [
             '1',
             '2',
             '3',
             '4'
         ]
         return Response({'message': 'ViewSet is called', 'ex_viewset': ex_viewset})
    
class MainApiView(APIView):
     """Test API View"""
     
     def get(self, request, format=None):
         an_apiview = [
             'A',
             'B',
             'C',
             'D'
         ]
         return Response({'message': 'View is called', 'an_apiview': an_apiview})

    # # Create your views here.


     def put(self, request, pk=None):
        return Response({'method': 'put'})

     def patch(self, request, pk=None):
        return Response({'method': 'patch' })

     def delete(self, request, pk=None):
        return Response({'method': 'delete' })    

class UserProfileViewSet(viewsets.ModelViewSet):
     """Handle creating, updating profiles"""

     serializer_class = serializers.UserProfileSerializer
     queryset = models.UserProfile.objects.all()
     authentication_classes = (TokenAuthentication,)
     permission_classes = (permissions.UpdateOwnProfile,)
     filter_backends = (filters.SearchFilter,)
     search_fields = ('name', 'email',)
     
class LoginViewSet(viewsets.ViewSet):
    """Check email and password and returns an auth token"""
    
    serializer_class = AuthTokenSerializer
    
    def create(self, request):
        """Use the ObtainAuthToken APIview to validate and create a token"""
        
        serializer = self.serializer_class(data=request.data,
                                            context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({'token': token.key})
    
class UserProfileFeedViewSet(ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.PostOwnStatus, IsAuthenticated)
    
    def perform_create(self, serializer):
        """"sets the user profile to the logged in user"""
        
        serializer.save(user_profile=self.request.user)