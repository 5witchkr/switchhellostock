from django.conf.urls import url
from .views import Login, Join, Logout

urlpatterns = [
    url('login', Login.as_view(), name='login'),
    url('join', Join.as_view(), name='join'),
    url('logout', Logout.as_view(), name='logout'),
]