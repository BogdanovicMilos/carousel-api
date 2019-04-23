from django.conf.urls import url
from .views import UserListAPIView, UserDetailAPIView

urlpatterns = [
    url(r'^$', UserListAPIView.as_view()),
    url(r'^(?P<id>\d+)/$', UserDetailAPIView.as_view()),
]
