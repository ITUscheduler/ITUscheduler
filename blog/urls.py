from django.urls import path
from .views import PostListView

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
]