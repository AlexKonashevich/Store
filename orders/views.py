from http import HTTPStatus

from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from decimal import Decimal

import orders.models
from Store import settings
from common.views import TitleMixin
from django.views.generic.base import TemplateView, HttpResponseRedirect
from orders.forms import OrdersForm
from orders.models import Order
import uuid
from yookassa import Payment

from products.models import Basket


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - Спасибо за заказ!'


class CanceledTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/cancel.html'
    title = 'Store - Заказ не оплачен.'


class OrderCreateView(CreateView, TitleMixin):
    template_name = 'orders/order-create.html'
    form_class = OrdersForm
    success_url = reverse_lazy('orders:order_create')
    title = 'Store - Оформление заказа'

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        order_id = uuid.uuid4()
        baskets = Basket.objects.filter(user=self.request.user)
        total_price = Decimal(0)
        goods = ''
        for basket in baskets:
            total_price += Decimal(basket.product.price) * Decimal(basket.quantity)
            goods += f'{basket.product.name} Количество: {basket.quantity}\n'
        payment = Payment.create({
            "amount": {
                "value": str(total_price),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "{}{}".format(settings.DOMAIN_NAME, reverse("orders:order_success"))
            },
            "metadata": {
                "user": self.request.user.username,
                "goods": goods
            },
            "capture": True,
            "description": f"Заказ №{order_id}"

        }, order_id)
        return HttpResponseRedirect(payment.confirmation.confirmation_url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)
