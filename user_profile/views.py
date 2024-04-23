from django.shortcuts import render, redirect
from orders.models import Order
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm
# Create your views here.
@login_required
def profile(request):

    current_user = request.user
    orders = Order.objects.filter(user=current_user)



    return render(request, 'user_profile/profile.html', {'current_user': current_user, 'orders': orders})

def edit(request):
    current_user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            return redirect('user_profile:profile')  # Перенаправляем пользователя на страницу профиля после успешного обновления

    else:
        form = UserUpdateForm(instance=current_user)

    return render(request, 'user_profile/edit.html', {'form': form})