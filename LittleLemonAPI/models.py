from typing import Iterable, Optional
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True, unique=True)

    def __str__(self) -> str:
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title)
        super().save(force_insert, force_update, using, update_fields)

class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.title


class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('menuitem', 'customer')


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_orders")
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="delivery_crew_orders", null=True)
    status = models.BooleanField(db_index=True, default=0)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(db_index=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderitems")
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name="orderitems")
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('order', 'menuitem')









