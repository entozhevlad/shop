from django.urls import path
from . import views
from reviews.views import delete_review, edit_review

app_name = 'shop'
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list,
         name='product_list_by_category'
         ),
    path('<int:id>/<slug:slug>', views.product_detail,
         name='product_detail'),
    path('<int:id>/<slug:slug>/delete_review/<int:review_id>/', delete_review, name='delete_review'),
    path('<int:id>/<slug:slug>/edit_review/<int:review_id>/', edit_review, name='edit_review'),


]