from django.shortcuts import Http404
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    UserRegisterSerializer,
    ObtainTokenPairSerializer,
    RiderSerializer,
    QuoteSerializer,
    OrderSerializer,
    InvoiceSerializer
)
from .permissions import IsAuthenticatedClient, IsAuthenticatedStaff, IsAuthenticatedClientOrStaff
from .models import Rider, Quote, Order, Invoice
User = get_user_model()

class UserRegisterView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = User(
                username = serializer.data['username'],
                first_name = serializer.data['first_name'],
                last_name = serializer.data['last_name'],
                email = serializer.data['email'],
                password = make_password(serializer.data['password']),
                bio = serializer.data['bio'],
                location = serializer.data['location']
            )
            user.save()
            return Response({
                'success': True,
                'message': 'User successfully created',
                'data': {
                    'username': serializer.data['username'],
                    'first_name': serializer.data['first_name'],
                    'last_name': serializer.data['last_name'],
                    'email': serializer.data['email'],
                    'date_joined': user.date_joined,
                    'bio': serializer.data['bio'],
                    'location': serializer.data['location']
                }
            },status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginTokenObtainPairView(TokenObtainPairView):
    serializer_class = ObtainTokenPairSerializer






# Rider Views
class RiderListView(APIView):
    '''
    Allow Staff to see riders
    '''
    permission_classes = [IsAuthenticatedStaff]

    def get(self, request, format=None):
        riders = Rider.objects.all()
        serializer = RiderSerializer(riders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        serializer = RiderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

class RiderDetailsView(APIView):
    permission_classes = [IsAuthenticatedStaff]

    def get_rider(self, id):
        try:
            return Rider.objects.get(pk=id)
        except Rider.DoesNotExist:
            raise(Http404)
    
    def error_response(self):
        return Response({
                'success': False,
                'message': 'The Rider does not exist',
                'data': []
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, id, format=None):
        try:
            rider = self.get_rider(id)
        except Http404:
            return self.error_response()

        serializer = RiderSerializer(rider)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, format=None):
        try:
            rider = self.get_rider(id)
        except Http404:
            return self.error_response()

        serializer = RiderSerializer(rider, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        try:
            rider = self.get_rider(id)
        except Http404:
            return self.error_response()

        if request.user.is_staff:
            rider.delete()
            return Response({
                'success': True,
                'message': 'Successfully deleted rider'
            }, status=status.HTTP_200_OK)
        return Response({
            'success': False,
            'message': "Cannot Delete , must be owner"
        }, status=status.HTTP_400_BAD_REQUEST)






# Quotes Views
class StaffQuoteListView(APIView):
    '''
    Allow Staff to view all quotes
    '''
    permission_classes = [IsAuthenticatedStaff]

    def get(self, request, format=None):
        quotes = Quote.objects.all()
        serializer = QuoteSerializer(quotes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class QuoteListView(APIView):
    '''
    Allow Clients to see their quotes
    '''
    permission_classes = [IsAuthenticatedClient]

    def get(self, request, format=None):
        quotes = Quote.objects.filter(user=request.user)
        serializer = QuoteSerializer(quotes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        serializer = QuoteSerializer(data=request.data)
        if serializer.is_valid():
            user = self.request.user
            serializer.save(user=user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

class QuoteDetailsView(APIView):
    permission_classes = [IsAuthenticatedClientOrStaff]

    def get_quote(self, id):
        try:
            return Quote.objects.get(pk=id)
        except Quote.DoesNotExist:
            raise(Http404)
    
    def error_response(self):
        return Response({
                'success': False,
                'message': 'The Quote does not exist',
                'data': []
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, id, format=None):
        try:
            quote = self.get_quote(id)
        except Http404:
            return self.error_response()

        serializer = QuoteSerializer(quote)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, format=None):
        try:
            quote = self.get_quote(id)
        except Http404:
            return self.error_response()

        serializer = QuoteSerializer(quote, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        try:
            quote = self.get_quote(id)
        except Http404:
            return self.error_response()

        if quote.user == request.user:
            quote.delete()
            return Response({
                'success': True,
                'message': 'Successfully deleted quote'
            }, status=status.HTTP_200_OK)
        return Response({
            'success': False,
            'message': "Cannot Delete , must be owner"
        }, status=status.HTTP_400_BAD_REQUEST)






# Order Views
class StaffOrderListView(APIView):
    '''
    Allow Staff to view all quotes
    '''
    permission_classes = [IsAuthenticatedStaff]

    def get(self, request, format=None):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderListView(APIView):
    permission_classes = [IsAuthenticatedClient]

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, quote_id, rider_id, format=None):
        try:
            quote = Quote.objects.get(pk=quote_id)
        except Quote.DoesNotExist:
            raise(Http404)
        
        rider = Rider.objects.get(pk=rider_id) or None

        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(rider=rider, quote=quote)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class OrderDetailsView(APIView):
    permission_classes = [IsAuthenticatedClientOrStaff]

    def get_order(self, id):
        try:
            return Order.objects.get(pk=id)
        except Order.DoesNotExist:
            raise(Http404)
    
    def error_response(self):
        return Response({
                'success': False,
                'message': 'The Order does not exist',
                'data': []
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, id, format=None):
        try:
            order = self.get_order(id)
        except Http404:
            return self.error_response()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, format=None):
        try:
            order = self.get_order(id)
        except Http404:
            return self.error_response()

        serializer = OrderSerializer(order, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# Invoice Views
class StaffInvoiceListView(APIView):
    '''
    Allow Staff to view all invoices
    '''
    permission_classes = [IsAuthenticatedStaff]

    def get(self, request, format=None):
        invoices = Invoice.objects.all()
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class InvoiceListView(APIView):
    permission_classes = [IsAuthenticatedClient]

    def get(self, request, format=None):
        invoices = Invoice.objects.filter(user=request.user)
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, quote_id, order_id, format=None):
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            raise(Http404)

        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(order=order, quote=order.quote)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class InvoiceDetailsView(APIView):
    permission_classes = [IsAuthenticatedClientOrStaff]

    def get_invoice(self, id):
        try:
            return Invoice.objects.get(pk=id)
        except Invoice.DoesNotExist:
            raise(Http404)
    
    def error_response(self):
        return Response({
                'success': False,
                'message': 'The Invoice does not exist',
                'data': []
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, id, format=None):
        try:
            invoice = self.get_invoice(id)
        except Http404:
            return self.error_response()

        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, format=None):
        try:
            invoice = self.get_invoice(id)
        except Http404:
            return self.error_response()

        serializer = InvoiceSerializer(invoice, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)