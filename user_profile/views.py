from django.shortcuts import render
from orders.models import Order
# Create your views here.
def profile(request):
    current_user = request.user
    orders = Order.objects.filter(user=current_user)
    return render(request, 'user_profile/profile.html', {'current_user': current_user, 'orders': orders})