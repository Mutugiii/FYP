from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UserRegisterView,
    LoginTokenObtainPairView,
    StaffQuoteListView,
    StaffOrderListView,
    StaffInvoiceListView,
    QuoteListView,
    QuoteDetailsView,
    OrderListView,
    OrderDetailsView,
    InvoiceListView,
    InvoiceDetailsView
)

urlpatterns = [
    path('register', UserRegisterView.as_view(), name='register'),
    path('login', LoginTokenObtainPairView.as_view(), name='login'),
    path('token/refresh', TokenRefreshView.as_view(), name='refresh_token'),
    path('staff/quotes', StaffQuoteListView.as_view(), name='staff_quotes'),
    path('staff/orders', StaffOrderListView.as_view(), name='staff_orders'),
    path('staff/invoices', StaffInvoiceListView.as_view(), name='staff_invoice'),
    path('quotes', QuoteListView.as_view(), name='quotes'),
    path('quote/<int:id>', QuoteDetailsView.as_view(), name='quote'),
    path('orders', OrderListView.as_view(), name='orders'),
    path('order/<int:id>', OrderDetailsView.as_view(), name='order'),
    path('invoices', InvoiceListView.as_view(), name='invoices'),
    path('invoice/<int:id>', InvoiceDetailsView.as_view(), name='invoice'),
]