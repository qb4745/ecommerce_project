from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.utils import timezone
from .models import Item, OrderItem, Order

# Create your views here.


class HomeListView(ListView):
    model = Item
    paginate_by = 5
    template_name = "core/home.html"


class ItemDetailView(DetailView):
    model = Item
    template_name = "core/product.html"


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Se ha añadido otra unidad a su carro.")
            return redirect("core:core-product", slug=slug)
        else:
            messages.info(request, "Este producto fue agregado a su carro.")
            order.items.add(order_item)
            return redirect("core:core-product", slug=slug)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Este producto fue agregado a su carro.")
        return redirect("core:core-product", slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            ).first()
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order_item.delete()
            messages.info(request, "La cantidad del producto fue actualizada.")
            return redirect("core:core-product", slug=slug)
        else:
            messages.info(request, "Este producto no estaba en su carro.")
            return redirect("core:core-product", slug=slug)
    else:
        messages.info(request, "No tienes un pedido activo.")
        return redirect("core:core-product", slug=slug)  # Using .first() instead of [0] to handle cases where the item doesn't exist
