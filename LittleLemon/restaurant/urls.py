from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('', views.index, name='index'),
    path('menu/', views.Menu_view),
    path('menu/<int:pk>', views.Singlemenu_view),
    path('groups/manager/users', views.Manager_view),
    path('groups/delivery-crew/users', views.Delivery_view),
    path('cart/menu-items', views.CartView.as_view()),
    path('orders', views.OrderView.as_view()),
    path('orders/<int:pk>', views.SingleOrderView.as_view()),
    path('api-token-auth/', obtain_auth_token),
]