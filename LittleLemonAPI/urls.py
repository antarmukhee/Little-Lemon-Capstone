from . import views
from django.urls import path, include

urlpatterns = [
    path('groups/manager/users', views.ManagerView.as_view()),
    path('groups/manager/users/<int:pk>', views.SingleManagerView.as_view()),
]