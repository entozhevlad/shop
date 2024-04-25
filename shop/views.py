from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from cart.forms import CartAddProductForm
from .models import Category, Product
from reviews.forms import ReviewForm
from reviews.models import Review

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_list_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html',
                  {
                      'category': category,
                      'categories': categories,
                      'products': products
                  })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    user_review = product.reviews.filter(user=request.user).exists()

    if request.method == 'POST':
        if not user_review:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.product = product
                review.save()
                return redirect('shop:product_detail', id=product.id, slug=product.slug)
        else:
            form = ReviewForm(instance=user_review)
    else:
        form = ReviewForm()
    reviews = product.reviews.all()
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {'product': product, 'cart_product_form': cart_product_form, 'form': form, 'reviews': reviews, 'user_review':user_review}, )

