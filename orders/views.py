from http import HTTPStatus

from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from decimal import Decimal

import json
from django.http import HttpResponse
from yookassa import Configuration
from yookassa.domain.notification import WebhookNotificationEventType, WebhookNotificationFactory
from yookassa.domain.common import SecurityHelper

from Store import settings
from common.views import TitleMixin
from django.views.generic.base import TemplateView, HttpResponseRedirect
from orders.forms import OrdersForm
from django.views.decorators.csrf import csrf_exempt
import uuid
from yookassa import Payment

from products.models import Basket
from orders.models import Order


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

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)

    def save_to_db(self, request):
        if request.method == "POST":
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            address = request.POST['address']
            data = OrdersForm(first_name=first_name, last_name=last_name, email=email, address=address)
            data.save()

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)
        total_price = Decimal(0)
        goods = ''
        orders = []
        # Order.objects.filter(id=self)

        order = '123'
        print(self.request.session.values())
        for i in orders:
            print(i.status)
            if i.status == 0:
                order = i
        print(order)
        order_id = 0
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
                "order_id": str(order_id),
                "user": self.request.user.username,
                "goods": goods
            },
            "capture": True,
            "description": f"Заказ № {order_id}"

        }, order_id)
        return HttpResponseRedirect(payment.confirmation.confirmation_url, status=HTTPStatus.SEE_OTHER)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@csrf_exempt
def yookassa_webhook(request):
    # Если хотите убедиться, что запрос пришел от ЮКасса, добавьте проверку:
    ip = get_client_ip(request)  # Получите IP запроса
    if not SecurityHelper().is_ip_trusted(ip):
        return HttpResponse(status=401)

    # Извлечение JSON объекта из тела запроса
    payload = request.body.decode('utf-8')
    event_json = json.loads(payload)
    try:
        # Создание объекта класса уведомлений в зависимости от события
        notification_object = WebhookNotificationFactory().create(event_json)
        response_object = notification_object.object
        if notification_object.event == WebhookNotificationEventType.PAYMENT_SUCCEEDED:
            some_data = {
                'paymentId': response_object.id,
                'paymentStatus': response_object.status,
            }
            order_id = event_json.metadata.order_id
            order = Order.objects.get(id=str(order_id))
            order.update_after_payment()
        elif notification_object.event == WebhookNotificationEventType.PAYMENT_WAITING_FOR_CAPTURE:
            some_data = {
                'paymentId': response_object.id,
                'paymentStatus': response_object.status,
            }
            # Специфичная логика
            # ...
        elif notification_object.event == WebhookNotificationEventType.PAYMENT_CANCELED:
            some_data = {
                'paymentId': response_object.id,
                'paymentStatus': response_object.status,
            }
            # Специфичная логика
            # ...
        else:
            # Обработка ошибок
            return HttpResponse(status=402)  # Сообщаем кассе об ошибке

        # Специфичная логика
        # ...
        Configuration.configure(settings.Configuration.account_id, settings.Configuration.secret_key)
        # Получим актуальную информацию о платеже
        payment_info = Payment.find_one(some_data['paymentId'])
        if payment_info:
            payment_status = payment_info.status
            # Специфичная логика
            print('paymentStatus', payment_status)
        else:
            # Обработка ошибок
            return HttpResponse(status=403)  # Сообщаем кассе об ошибке

    except Exception:
        # Обработка ошибок
        return HttpResponse(status=404)  # Сообщаем кассе об ошибке

    return HttpResponse(status=200)  # Сообщаем кассе, что все хорошо
