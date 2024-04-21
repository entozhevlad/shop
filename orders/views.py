from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse
from django.shortcuts import render, redirect

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # Очистка корзины
            cart.clear()
            order_created.delay(order.id)
            request.session['order_id'] = order.id
            return redirect(reverse('payments:process'))
    else:
        form = OrderCreateForm()
    return render(request, 'orders/create.html',
                  {'cart': cart, 'form': form})
