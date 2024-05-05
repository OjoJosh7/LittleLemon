from django.shortcuts import render, get_object_or_404
from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .models import MenuItem, Category, Cart, Order, OrderItem
from .serializers import MenuItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer, UserSerilializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User, Group
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def Menu_view(request):
    if(request.method=='GET'):
       item = MenuItem.objects.select_related('category').all()
       serializer_item = MenuItemSerializer(item, many=True)
       return Response(serializer_item.data, status.HTTP_200_OK)
    
    elif(request.method=='POST'):
        if request.user.groups.filter(name='Manager').exists():
            serializer_item = MenuItemSerializer(data=request.data)
            serializer_item.is_valid(raise_exception=True) 
            serializer_item.save()
            return Response(serializer_item.validated_data, status.HTTP_201_CREATED)
        else:
            return Response('You don\'t have the authorization!',status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET', 'PUT', 'PATCH','DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def Singlemenu_view(request, pk):
    try: 
        menu = MenuItem.objects.get(pk=pk) 
    except MenuItem.DoesNotExist: 
        return Response(status=status.HTTP_404_NOT_FOUND) 
  
    if request.method == 'GET': 
        serializer = MenuItemSerializer(menu) 
        return Response(serializer.data, status.HTTP_200_OK) 
  
    elif request.method == 'PUT': 
        if request.user.groups.filter(name='Manager').exists():
            serializer = MenuItemSerializer(menu, data=request.data) 
  
            if serializer.is_valid(): 
                serializer.save() 
                return Response(serializer.data, status.HTTP_200_OK) 
            return Response(serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response('You don\'t have the authorization!',status=status.HTTP_401_UNAUTHORIZED)
    elif request.method == 'PATCH': 
        if request.user.groups.filter(name='Manager').exists():
            serializer = MenuItemSerializer(menu, 
                                           data=request.data, 
                                           partial=True) 
  
            if serializer.is_valid(): 
                serializer.save() 
                return Response(serializer.data, status.HTTP_200_OK) 
            return Response(serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response(status.HTTP_403_UNAUTHORIZED)
  
    elif request.method == 'DELETE': 
        if request.user.groups.filter(name='Manager').exists():
           menu.delete() 
           return Response(status=status.HTTP_204_NO_CONTENT) 
        else:
            return Response('You don\'t have the authorization!',status=status.HTTP_401_UNAUTHORIZED)
    



@api_view(['GET', 'POST', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAdminUser])
def Manager_view(request): 
    if request.method == 'GET':
        users = User.objects.all().filter(groups__name='Manager')
        managers = UserSerilializer(users, many=True)
        return Response(managers.data, status.HTTP_200_OK)
    elif request.method == 'POST':
        username = request.data['username']
        if username:
           user = get_object_or_404(User, username=username)
           managers = Group.objects.get(name = 'Manager')
           managers.user_set.add(user)
           return Response(status.HTTP_201_CREATED)
        return Response(status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        username = request.data['username']
        if username:
           user = get_object_or_404(User, username=username)
           managers = Group.objects.get(name = 'Manager')
           managers.user_set.remove(user)
           return Response(status.HTTP_200_OK)
        return Response(status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAdminUser])
def Delivery_view(request):  
    if request.method == 'GET':
        users = User.objects.all().filter(groups__name='Delivery Crew')
        delivery_crew = UserSerilializer(users, many=True)
        return Response(delivery_crew.data, status.HTTP_200_OK)
        
    if request.method == 'POST':
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            delivery_crew = Group.objects.get(name = 'Delivery Crew')
            delivery_crew.user_set.add(user)
            return Response(status.HTTP_201_CREATED)
        return Response(status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        username = request.data['username']
        if username:
           user = get_object_or_404(User, username=username)
           delivery_crew = Group.objects.get(name = 'Delivery Crew')
           delivery_crew.user_set.remove(user)
           return Response(status.HTTP_200_OK)
        return Response(status.HTTP_400_BAD_REQUEST)
    
   


class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.all().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        Cart.objects.all().filter(user=self.request.user).delete()
        return Response("ok")
    
class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        elif self.request.user.groups.count()==0: #normal customer - no group
            return Order.objects.all().filter(user=self.request.user)
        elif self.request.user.groups.filter(name='Delivery Crew').exists(): #delivery crew
            return Order.objects.all().filter(delivery_crew=self.request.user)  #only show oreders assigned to him
        else: #delivery crew or manager
            return Order.objects.all()
        # else:
        #     return Order.objects.all()
    
    def create(self, request, *args, **kwargs):
        menuitem_count = Cart.objects.all().filter(user=self.request.user).count()
        if menuitem_count == 0:
            return Response({"message:": "no item in cart"})

        data = request.data.copy()
        total = self.get_total_price(self.request.user)
        data['total'] = total
        data['user'] = self.request.user.id
        order_serializer = OrderSerializer(data=data)
        if (order_serializer.is_valid()):
            order = order_serializer.save()

            items = Cart.objects.all().filter(user=self.request.user).all()

            for item in items.values():
                orderitem = OrderItem(
                    order=order,
                    menuitem_id=item['menuitem_id'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
                orderitem.save()
            Cart.objects.all().filter(user=self.request.user).delete() #Delete cart items

            result = order_serializer.data.copy()
            result['total'] = total
            return Response(order_serializer.data)
    
    def get_total_price(self, user):
        total = 0
        items = Cart.objects.all().filter(user=user).all()
        for item in items.values():
            total += item['price']
        return total
    
class SingleOrderView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if self.request.user.groups.count()==0: # Normal user, not belonging to any group = Customer
            return Response('Not Ok')
        else: #everyone else - Super Admin, Manager and Delivery Crew
            return super().update(request, *args, **kwargs)

