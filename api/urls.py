from django.urls import path
from .views import SearchOrdersView, SearchCustomersView, CreateCustomerView, UpdateCustomerView

urlpatterns = [
    path('orders', SearchOrdersView.as_view(), name='search-orders'),
    path("customers", SearchCustomersView.as_view(), name="search-customers"),
    path("customers/create", CreateCustomerView.as_view(), name="create-customer"),
    path("customers/<str:customerid>",
         UpdateCustomerView.as_view(), name="update-customer"),
]
