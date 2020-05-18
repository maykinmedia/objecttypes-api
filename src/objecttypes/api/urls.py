from django.conf.urls import include, url

from rest_framework import routers

from .views import ObjectTypeViewSet

router = routers.DefaultRouter()
router.register(r"objecttypes", ObjectTypeViewSet)

urlpatterns = [url("v1/", include([url("", include(router.urls))]),)]
