from http import HTTPStatus

from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse

from Store import settings
from common.views import TitleMixin
from django.views.generic.base import TemplateView, HttpResponseRedirect
from orders.forms import OrdersForm
import uuid

from yookassa import Payment


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
        payment = Payment.create({
            "amount": {
                "value": "100.00",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": '{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success'))
            },
            "capture": True,
            "description": "Заказ №1"

        }, uuid.uuid4())
        return HttpResponseRedirect(payment.confirmation.confirmation_url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)
