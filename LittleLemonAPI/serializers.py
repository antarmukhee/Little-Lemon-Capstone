from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, MenuItem, Order, OrderItem, Cart
from django.shortcuts import get_object_or_404


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'slug', 'title')
        read_only_fields = ('slug', )


class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only = True)
    category_id = serializers.IntegerField(write_only = True)
    class Meta:
        model = MenuItem
        fields = ('id', 'title', 'price', 'featured', 'category', 'category_id')


class CartSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only = True)
    menuitem = MenuItemSerializer(read_only = True)
    menuitem_id = serializers.IntegerField(write_only = True)
    class Meta:
        model = Cart
        fields = ('id', 'customer', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price')
        read_only_fields = ('unit_price', 'price')
    def validate(self, attrs):
        menu_item = get_object_or_404(MenuItem, pk=attrs['menuitem_id'])
        attrs['unit_price'] = menu_item.price
        attrs['price'] = attrs['quantity'] * attrs['unit_price']
        attrs['customer_id'] = self.context['request'].user.id
        return attrs
    

class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only = True)
    menuitem_id = serializers.IntegerField(write_only = True)
    class Meta:
        model = OrderItem
        fields = ('id', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price')


class OrderSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only = True)
    customer_id = serializers.IntegerField(write_only = True)
    delivery_crew = UserSerializer(read_only = True)
    delivery_crew_id = serializers.IntegerField(write_only = True)
    orderitems = OrderItemSerializer(read_only=True, many=True)
    class Meta:
        model = Order
        fields = ('id', 'customer', 'customer_id', 'delivery_crew', 'delivery_crew_id', 'status', 'total', 'date', 'orderitems')






