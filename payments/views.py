from decimal import Decimal
import stripe
from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from orders.models import Order
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

# создать экземпляр Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        success_url = request.build_absolute_uri(
            reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payments:canceled'))
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': [],
        }
        total_amount = int(order.get_total_cost() * 100)  # Общая стоимость заказа
        session_data['line_items'].append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Total',
                },
                'unit_amount': total_amount,
            },
            'quantity': 1,
        })
        session = stripe.checkout.Session.create(**session_data)
        return redirect(session.url, code=303)
    else:
        return render(request, 'payments/process.html', locals())


def payment_completed(request):
    return render(request, 'payments/completed.html')
def payment_canceled(request):
    return render(request, 'payments/canceled.html')


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = json.loads(payload)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session['client_reference_id']
        order = Order.objects.get(id=order_id)
        # Обновите статус заказа на "оплаченный"
        order.paid = True
        order.save()

    return HttpResponse(status=200)
