from rest_framework import serializers
from . import models

class SerializerTest(serializers.Serializer):
    name = serializers.CharField(max_length=10)

class UserProfileSerializer(serializers.ModelSerializer):
    """"A serializer for out user profile objects"""    

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Create and return a new user"""

        user = models.UserProfile(
            email=validated_data['email'],
            name = validated_data['name']
        )    

        user.set_password(validated_data['password'])
        user.save()

        return user
    
class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """"A serializer for profile feed items objects"""    

    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        extra_kwargs = {'user_profile': {'read_only': True}}
        
class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'age': instance.age
        }     
        
class AllDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SewingEfficiency
        fields = '__all__'

    def to_representation(self, instance):
        return {
             'sc': instance.sc,
            'style': instance.style,
            'buyer': instance.buyer,
            'smv': str(instance.smv),
            'working_hrs': instance.working_hrs,
            'line_balance_count': instance.line_balance_count,
            'othrs': str(instance.othrs),
            'produce_mins': str(instance.produce_mins),
            'use_mins': str(instance.use_mins),
            'location': instance.location,
            'create_date': instance.create_date,
            'line_no': instance.line_no,
            'actual_efficiency': str(instance.actual_efficiency),
            'planned_efficiency': str(instance.planned_efficiency),
            'pqty': instance.pqty,
            'component': instance.component,
            'plan_qty': instance.plan_qty,
            'plan_smv': instance.plan_smv,
            'plan_efficiency': str(instance.plan_efficiency),
            'sec_id': instance.sec_id,
            'shift': instance.shift,
            'date_time': instance.date_time,
            'timestamp': instance.timestamp,
            'ordertype': instance.ordertype,
            'aql_fail': instance.aql_fail,
            'cni_fail': instance.cni_fail,
            'prod_day': instance.prod_day
        }                