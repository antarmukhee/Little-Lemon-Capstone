from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth.models import Group, User
from .serializers import UserSerializer
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser

# Create your views here.

class ManagerView(generics.ListCreateAPIView):

    permission_classes = (IsAdminUser,)
    
    def get_queryset(self):
        if self.request.method == 'POST': queryset = None
        else: queryset = User.objects.filter(groups__name='Manager')
        return queryset
    
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        current_user = self.request.POST.get("username")
        if not current_user: raise NotFound
        current_user = get_object_or_404(User, username = current_user)
        manager_group = Group.objects.get(name='Manager')
        current_user.groups.add(manager_group)
        return Response(status=status.HTTP_201_CREATED)


    



