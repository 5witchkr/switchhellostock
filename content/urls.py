from django.conf.urls import url
from django.urls import path
from .views import Main, CreateMain, Detail, UploadReply, DeleteReply

urlpatterns = [
    path('main<int:page>', Main.as_view(), name='main'),
    path('create', CreateMain.as_view(), name='create'),
    path('detail<int:id>', Detail.as_view(), name='detail'),
    path('uploadreply', UploadReply.as_view(), name='uploadreply'),
    path('deletereply', DeleteReply.as_view(), name='deletereply')
]