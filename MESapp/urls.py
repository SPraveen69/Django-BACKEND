from django.urls import re_path
from. import views
from rest_framework.routers import DefaultRouter
from django.conf.urls import include

router = DefaultRouter()
router.register('viewset', views.MainApiViewSet, basename='set')
router.register('profile', views.UserProfileViewSet)
router.register('login', views.LoginViewSet, basename='login')
# router.register('logout', views.LogoutViewSet, basename='logout')
router.register('feed', views.UserProfileFeedViewSet, basename='feed')
router.register('csv-data', views.CsvDataViewSet, basename='csv-data')
router.register('popular-styles', views.StyleDataViewSet, basename='popular-styles')
router.register('style-wise', views.StyleWiseDataViewSet, basename='style-wise')
router.register('stylewise-all', views.StyleAllDataViewSet, basename='stylewise-all')
router.register('allFactor', views.AllFatorDataViewSet, basename='allFactor')
router.register('logout', views.LogoutApiViewSet, basename='logout')
#router.register('predict', views.PredictEfficiencyViewSet, basename='predict')

urlpatterns = [
    re_path(r'^view/', views.MainApiView.as_view()),
    #re_path(r'^getData/$', views.DataRetrieveViewSet.as_view({'get': 'list'}), name='getData-list'),
    re_path('', include(router.urls)),
    re_path(r'^predict/$', views.predict, name='predict'),
    re_path(r'^logout', views.logout, name='logout'),
]