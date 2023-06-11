from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth.models import Group, User
from .serializers import UserSerializer
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import IsManager, IsCustomer, IsAuthenticatedAndReadOnly
from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer

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
        return Response(data = {"message" : "user added to the manager group"}, status=status.HTTP_200_OK)
    

class SingleManagerView(generics.DestroyAPIView):

    permission_classes = (IsAdminUser,)

    def delete(self, request, pk):
        current_user = get_object_or_404(User, pk = pk)
        manager_group = Group.objects.get(name='Manager')
        current_user.groups.remove(manager_group)
        return Response(data = {"message" : "user deleted from the manager group"}, status=status.HTTP_200_OK)
    

class CrewView(generics.ListCreateAPIView):

    permission_classes = (IsManager|IsAdminUser,)
    
    def get_queryset(self):
        if self.request.method == 'POST': queryset = None
        else: queryset = User.objects.filter(groups__name='Delivery crew')
        return queryset
    
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        current_user = self.request.POST.get("username")
        if not current_user: raise NotFound
        current_user = get_object_or_404(User, username = current_user)
        crew_group = Group.objects.get(name='Delivery crew')
        current_user.groups.add(crew_group)
        return Response(data = {"message" : "user added to the delivery crew group"}, status=status.HTTP_200_OK)
    

class SingleCrewView(generics.DestroyAPIView):

    permission_classes = (IsManager|IsAdminUser,)

    def delete(self, request, pk):
        current_user = get_object_or_404(User, pk = pk)
        crew_group = Group.objects.get(name='Delivery crew')
        current_user.groups.remove(crew_group)
        return Response(data = {"message" : "user deleted from the delivery crew group"}, status=status.HTTP_200_OK)
    

class CategoryView(generics.ListCreateAPIView):

    permission_classes = (IsAdminUser,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MenuItemView(generics.ListCreateAPIView):

    permission_classes = (IsManager|IsAdminUser|IsAuthenticatedAndReadOnly,)
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = (IsManager|IsAdminUser|IsAuthenticatedAndReadOnly,)
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer


class CartView(generics.ListCreateAPIView, generics.DestroyAPIView):
    
    permission_classes = (IsCustomer|IsAdminUser,)
    def get_queryset(self):
        return Cart.objects.filter(customer = self.request.user)
    serializer_class = CartSerializer

    def delete(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(customer = request.user)
        for item in cart_items:
            item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class OrderView(generics.ListCreateAPIView):

    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name = 'Manager'): return Order.objects.all()
        elif user.groups.filter(name = 'Delivery crew'): return Order.objects.filter(delivery_crew=user)
        else: return Order.objects.filter(customer=user)
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        order_id = serializer.data.get('id')
        cart_items = Cart.objects.filter(customer=request.user)
        for item in cart_items:
            OrderItem(
                order_id=order_id,
                menuitem=item.menuitem,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.price,
            ).save()
            item.delete()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    



        


    







    



