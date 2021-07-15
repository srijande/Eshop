from django.urls import path,include
from django.contrib import admin
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
# router.register(r'providers', api_views.ProviderViewSet)
# router.register(r'requests', api_views.RequestViewSet)
# router.register(r'services', api_views.ServiceViewSet)



urlpatterns = [
        #Leave as empty string for base url
	path('', views.store, name="store"),
    path('api/', include('rest_framework.urls')),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),
	path('login/', views.loginpage, name="login"),
	path('logout/', views.logout_view, name="logout"),
	path('processOrder/', views.processOrder, name="processOrder"),
	path('register/', views.register, name="register"),
    
]