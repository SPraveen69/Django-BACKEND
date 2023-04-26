from django.urls import re_path
from. import views
from rest_framework.routers import DefaultRouter
from django.conf.urls import include

router = DefaultRouter()
router.register('viewset', views.MainApiViewSet, basename='set')
router.register('profile', views.UserProfileViewSet)
router.register('login', views.LoginViewSet, basename='login')
router.register('feed', views.UserProfileFeedViewSet, basename='feed')


urlpatterns = [
    re_path(r'^view/', views.MainApiView.as_view()),
    re_path(r'', include(router.urls)),

]