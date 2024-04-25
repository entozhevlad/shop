from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from .models import Review
from .forms import ReviewForm
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user == request.user:
        review.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def edit_review(request, id, slug, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('shop:product_detail', id=id, slug=slug)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'shop/product/edit_review.html', {'form': form})


