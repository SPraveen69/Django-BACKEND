from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
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
from django.contrib.auth import logout
from django.db import connection
from django.http import HttpResponse
from django.db.models import Count
from django.db.models.functions import Cast
from django.db.models.fields import DateField
from django.db.models import Avg
import pickle
from rest_framework.renderers import JSONRenderer

from .models import Person
from .models import SewingEfficiency

from . import serializers
from . import models
from . import permissions
import csv
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import redirect

import pandas as pd
import logging

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def predict(request):
    
        logger = logging.getLogger(__name__)
    # Load the pickled model
        with open('C:/IIT/Implementation/Django/FYP/MES/MESapp/test.pkl', 'rb') as f:
            model = pickle.load(f)
    
        # Get the query parameters from the request
        style = request.GET.get('style')
        create_date = request.GET.get('create_date')
        pqty = request.GET.get('pqty')
        
        planned_efficiency = SewingEfficiency.objects.using('test').filter(style=style).aggregate(Avg('planned_efficiency'))['planned_efficiency__avg']
        smv = SewingEfficiency.objects.using('test').filter(style=style).aggregate(Avg('smv'))['smv__avg']
        working_hrs =  SewingEfficiency.objects.using('test').filter(style=style).aggregate(Avg('working_hrs'))['working_hrs__avg']
        produce_mins = SewingEfficiency.objects.using('test').filter(style=style).aggregate(Avg('produce_mins'))['produce_mins__avg']
        use_mins = SewingEfficiency.objects.using('test').filter(style=style).aggregate(Avg('use_mins'))['use_mins__avg']
        location = SewingEfficiency.objects.using('test').filter(style=style).aggregate(Avg('location'))['location__avg']
        
         # Log the values retrieved from the database
        logger.debug(f'style: {style}')
        logger.debug(f'working_hrs: {working_hrs}')
        logger.debug(f'produce_mins: {produce_mins}')
        logger.debug(f'use_mins: {use_mins}')
        logger.debug(f'location: {location}')
        logger.debug(f'create_date: {create_date}')
        logger.debug(f'planned_efficiency: {planned_efficiency}')
        logger.debug(f'pqty: {pqty}')

        # Create a pandas dataframe with the input data
        
        data = {'style': [float(2.0)],
                'smv': [float(smv)],
                'working_hrs': [float(working_hrs)],
                'produce_mins': [float(produce_mins)],
                'use_mins': [float(use_mins)],
                'location': [float(location)],
                'create_date': [float(create_date)],
                'planned_efficiency': [float(planned_efficiency)],
                'pqty': [float(pqty)]}
        input_data = pd.DataFrame(data)
        
        # Make the prediction using the model
        predicted_efficiency = model.predict(input_data)[0]
        
        # # Save the prediction to the database
        # prediction = Prediction(style=style, smv=smv, working_hrs=working_hrs, produce_mins=produce_mins,
        #                          use_mins=use_mins, location=location, create_date=create_date,
        #                          planned_efficiency=planned_efficiency, pqty=pqty,
        #                          predicted_efficiency=predicted_efficiency)
        # prediction.save()
        
        # Return the predicted efficiency as a JSON response
        response = {'predicted_efficiency': predicted_efficiency}
        return Response(response)
    
def logout(request):
    request.user.auth_token.delete()
    logout(request)
    return redirect('login')
    
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
        
        return Response({
            'token': token.key,
            'email': user.email,
            'user_id': user.pk})

class LogoutApiViewSet(viewsets.ViewSet):
    def destroy(self, request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')
            
    
class UserProfileFeedViewSet(ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.PostOwnStatus, IsAuthenticated)
    #perform test
    def perform_create(self, serializer):
        """"sets the user profile to the logged in user"""
        
        serializer.save(user_profile=self.request.user)
        
class CsvDataViewSet(viewsets.ViewSet):
    
    def list(self, request):
        try:
            with open('C:/IIT/Implementation/Angular new update/MES_FRONT_END/src/assets/csv/RU5733W.csv', 'r') as file:
                reader = csv.DictReader(file)
                csv_data = [row for row in reader]
            return Response(csv_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class StyleWiseDataViewSet(viewsets.ViewSet):
    serializer_class = serializers.AllDataSerializer
    def list(self, request):
        data = SewingEfficiency.objects.using('test').filter(style='1127694').values('create_date', 'actual_efficiency')
        #serializer = self.serializer_class(data, many=True)
        return Response(data)    

class StyleDataViewSet(viewsets.ViewSet):
    
    def list(self, request):
        persons = Person.objects.using('test').all()
        Data = SewingEfficiency.objects.using('test').values('style').annotate(
        style_count=Count('style')
        ).filter(style_count__gte=2).values(
        'style'
        ).distinct().annotate(
        count=Count('style')
        )

        # create a list of dictionaries with the style and count values
        # result = [{'style': item['style'], 'count': item['count']} for item in Data]

    # return a JSON response with the result
        return Response({'style': item['style']} for item in Data)
  
class StyleAllDataViewSet(viewsets.ViewSet):
    # def create(self, request):
    #     style = self.request.GET.get('style', '')
    #     if style is not None:
    #         queryset = SewingEfficiency.objects.using('test').filter(style=style)
    #     else:
    #         queryset = SewingEfficiency.objects.using('test').all()
    #     data = list(queryset.values())
    #     return Response(data)
    
    # def list(self, request):
    #     style = request.GET.get('style', '')
    #     if style is not None:
    #         queryset = SewingEfficiency.objects.using('test').filter(style=style).values_list('actual_efficiency')
    #     else:
    #         queryset = SewingEfficiency.objects.using('test').all()
    #     data = list(queryset.values())
    #     return Response(data)


    def list(self, request):
        style = request.GET.get('style', '')
        if style:
            queryset = SewingEfficiency.objects.using('test').filter(style=style).values_list('style','create_date','actual_efficiency')
        else:
            queryset = SewingEfficiency.objects.using('test').all().values_list('create_date','actual_efficiency')
            
        grouped_queryset = queryset.annotate(date=Cast('create_date', output_field=DateField())).values('create_date').annotate(actual_efficiency_avg=Avg('actual_efficiency'))
        data = list(grouped_queryset)
        return Response(data)


        # style = request.GET.get('style', '')
        # if style:
        #     queryset = SewingEfficiency.objects.using('test').filter(style=style).values_list('style','create_date', 'actual_efficiency')
        # else:
        #     queryset = SewingEfficiency.objects.using('test').all().values_list('style','create_date', 'actual_efficiency')
    
        # # Filter out zero and negative values
        # queryset = queryset.filter(actual_efficiency__gt=0)
            
        # grouped_queryset = queryset.annotate(date=Cast('create_date', output_field=DateField())).values('create_date').annotate(actual_efficiency_avg=Avg('actual_efficiency')).order_by('-create_date')
        # data = list(grouped_queryset)
        # return Response(data)   
    
class AllFatorDataViewSet(viewsets.ViewSet):
    
    def list(self, request):
        factors = request.GET.get('factor', '')
        if factors:
            queryset = SewingEfficiency.objects.using('test').values_list('create_date', factors)
        else:
            queryset = SewingEfficiency.objects.using('test').all()
            
        grouped_queryset = queryset.annotate(date=Cast('create_date', output_field=DateField())).values('create_date').annotate(value_avg=Avg(factors))
        data = list(grouped_queryset)
        return Response(data)
    
#
    
    
    