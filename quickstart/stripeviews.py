import json
import stripe

from decimal import Decimal

from django.conf import settings
from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import ItemModel,OrderModel

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request):
    data = json.loads(request.body)
    item_ids = data.get('item_ids', [])
    rates = { "usd" : Decimal("1"), "eur": Decimal("0.93"), "rub": Decimal("75.2") } 

    if not item_ids:
        return JsonResponse({'error' : 'Товары не переданы'},
                            status = 422)
    
    items = ItemModel.objects.filter(
        id__in=item_ids,
        orders__user=request.user,
        orders__is_paid=False
    ).distinct()
    
    if not items.exists():
        return JsonResponse(
            {'error' : 'Товары не найдены'},
            status = 404
        )
    
    line_items = []
    currency = data.get('currency', 'usd').lower()
    
    for item in items:
        line_items.append({
            'price_data' : {
                "currency": currency,
                "product_data" :{
                    'name' : item.name,
                },
                'unit_amount' : int(item.price * rates[currency] * 100),
            },
            'quantity' : 1,
        })

    session = stripe.checkout.Session.create(
        mode = 'payment',
        payment_method_types=['card'],
        line_items=line_items,
        success_url='http://localhost:8000/success_payment/',
        cancel_url='http://localhost:8000/cancle_payment/',
        metadata={
        "item_ids": ",".join(map(str, items.values_list("id", flat=True)))
        }
    )
    return JsonResponse({"url": session.url})

@csrf_exempt
def webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        print(e)
        return HttpResponse(status = 400)
    
    if event['type'] == "checkout.session.completed":
        session = event['data']['object']
        item_ids = session['metadata']['item_ids'].split(',')

        OrderModel.objects.filter(
            items__id__in=item_ids,
            is_paid=False
        ).update(is_paid=True)

    return HttpResponse(status =200)


def success_payment(request):
    return render(request, 'quickstart/stripe/success_payment.html')

def cancle_payment(request):
    return render(request, 'quickstart/stripe/cancle_payment.html')