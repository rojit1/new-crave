from api.views.product import CustomerProductAPI, ProductList, ProductDetail,ProductMultipriceapi, ProductTypeListView
from django.urls import path

from rest_framework import routers

router = routers.DefaultRouter()
router.register("customer-product-list", CustomerProductAPI)

urlpatterns = [
    path('category-list/', ProductTypeListView.as_view(), name="api_category_list"),
    path("product-list/", ProductList.as_view(), name="api_product_list"),
    path("product-detail/<int:pk>", ProductDetail.as_view(), name="api_product_detail"), 
    path("product-prices/", ProductMultipriceapi.as_view(), name="api_product_price"), 
] + router.urls

