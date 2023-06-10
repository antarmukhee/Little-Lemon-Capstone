from . import views
from django.urls import path

urlpatterns = [
    path('groups/manager/users', views.ManagerView.as_view()),
    path('groups/manager/users/<int:pk>', views.SingleManagerView.as_view()),
    path('groups/delivery-crew/users', views.CrewView.as_view()),
    path('groups/delivery-crew/users/<int:pk>', views.SingleCrewView.as_view()),
    path('categories', views.CategoryView.as_view()),
    path('menu-items', views.MenuItemView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('cart/menu-items', views.CartView.as_view()),

]