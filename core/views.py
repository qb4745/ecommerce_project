from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import View
from .forms import CheckoutForm
from .models import Item, OrderItem, Order, BillingAddress

# Create your views here.
class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, 'core/checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_adress = form.cleaned_data.get("street_adress")
                apartment_adress = form.cleaned_data.get("apartment_adress")
                country =form.cleaned_data.get("country")
                zip = form.cleaned_data.get("zip")
                # TODO: add functionality for these fields
                # same_shipping_adress = form.cleaned_data.get("same_shipping_adress")
                # save_info = form.cleaned_data.get("save_info")
                payment_option = form.cleaned_data.get("payment_option")
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_adress=street_adress,
                    apartment_adress=apartment_adress,
                    country=country,
                    zip=zip
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                # TODO: redirect to the selected payment option
                return redirect('core:core-checkout')
            messages.warning(self.request, "Error al enviar el formulario.")
            return redirect('core:core-checkout')

        except ObjectDoesNotExist:
            messages.warning(self.request, "No tienes un pedido activo.")
            return redirect("core:core-order-summary")


class PaymentView(View):
    def get(self, *args, **kwargs):
        return render(self.request, "core/payment.html")


class HomeListView(ListView):
    model = Item
    paginate_by = 5
    template_name = "core/home.html"






class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                "object": order
            }
            return render(self.request, "core/order_summary.html", context)

        except ObjectDoesNotExist:
            messages.warning(self.request, "No tienes un pedido activo.")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    template_name = "core/product.html"


@login_required
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
            return redirect("core:core-order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "Este producto fue agregado a su carro.")
            return redirect("core:core-order-summary")

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Este producto fue agregado a su carro.")
        return redirect("core:core-order-summary")


@login_required
def remove_single_item_from_cart(request, slug):
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
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "La cantidad del producto fue actualizada.")
            return redirect("core:core-order-summary")
        else:
            messages.info(request, "Este producto no estaba en su carro.")
            return redirect("core:core-order-summary", slug=slug)
    else:
        messages.info(request, "No tienes un pedido activo.")
        return redirect("core:core-order-summary", slug=slug)  # Using .first() instead of [0] to handle cases where the item doesn't exist


@login_required
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
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "La cantidad del producto fue actualizada.")
            return redirect("core:core-order-summary")
        else:
            messages.info(request, "Este producto no estaba en su carro.")
            return redirect("core:core-product", slug=slug)
    else:
        messages.info(request, "No tienes un pedido activo.")
        return redirect("core:core-order-summary")  # Using .first() instead of [0] to handle cases where the item doesn't exist