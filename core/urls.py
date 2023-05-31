from django.urls import path
from .views import (
    HomeListView,
    OrderSummaryView,
    ItemDetailView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
)

app_name = 'core'

urlpatterns = [
    path('', HomeListView.as_view(), name="core-home"),
    path('order-summary/', OrderSummaryView.as_view(), name='core-order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='core-product'),
    path('add-to-cart/<slug>/', add_to_cart, name='core-add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='core-remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name='core-remove-single-item-from-cart'),

]