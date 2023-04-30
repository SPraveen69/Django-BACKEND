from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

# Create your models here.

from django.db import models


class UserProfileManager(BaseUserManager):
    """Helps Django work with the custom model"""

    def create_user(self, email, name, password=None):
        """Create a new user profile object"""

        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, name, password):
        """Creates and saves a new superuser"""

        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        
        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Represents a "user Profile" inside the system"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Used to get users full name"""

        return self.name

    def get_short_name(self):
        """Used to get users short name"""

        return self.name
    
    def __str__(self):
        """Django uses this when it needs to convert object to string"""

        return self.email
    
class ProfileFeedItem(models.Model):
    """Profile status update"""
    
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        """return the model as a string"""
        
        return self.status_text
    
class SewingEfficiency(models.Model):
    sc = models.IntegerField(blank=True)
    style = models.CharField(max_length=255, blank=True)
    buyer = models.CharField(max_length=255, blank=True)
    smv = models.DecimalField(decimal_places=10, max_digits=10, blank=True)
    working_hrs = models.CharField(max_length=255, blank=True, default='')
    line_balance_count = models.CharField(max_length=255, blank=True)
    othrs = models.DecimalField(decimal_places=10, max_digits=10, blank=True)
    produce_mins = models.DecimalField(decimal_places=10, max_digits=10,  blank=True, default='')
    use_mins = models.DecimalField(decimal_places=10, max_digits=10, blank=True)
    location = models.CharField(max_length=255, blank=True)
    create_date = models.CharField(max_length=255, blank=True)
    line_no = models.CharField(max_length=255, blank=True)
    actual_efficiency = models.DecimalField(decimal_places=10, max_digits=10, blank=True)
    planned_efficiency = models.DecimalField(decimal_places=10, max_digits=10, blank=True)
    pqty = models.IntegerField(blank=True)
    component = models.CharField(max_length=255, blank=True)
    plan_qty = models.CharField(max_length=255, blank=True)
    plan_smv = models.CharField(max_length=255, blank=True)
    plan_efficiency = models.DecimalField(decimal_places=10, max_digits=10, blank=True)
    sec_id = models.CharField(max_length=255, blank=True)
    shift = models.CharField(max_length=255, blank=True)
    date_time = models.CharField(max_length=255, blank=True)
    timestamp = models.CharField(max_length=255, blank=True)
    ordertype = models.CharField(db_column='orderType', max_length=255, blank=True)  # Field name made lowercase.
    aql_fail = models.CharField(max_length=255, blank=True)
    cni_fail = models.CharField(max_length=255, blank=True)
    prod_day = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = True
        db_table = "Sewing_Efficiency"

class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    
    class Meta:
        managed = True
        db_table = "mesapp_person"
    # def __str__(self):
    #     return self.name
