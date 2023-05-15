from django.forms.models import model_to_dict
from rest_framework.response import Response
from api.serializers.product import (
    CustomerProductDetailSerializer,
    CustomerProductSerializer,
    ProductSerializer,
    ProductCategorySerializer
)
from rest_framework.views import exception_handler

from rest_framework.generics import ListAPIView, RetrieveAPIView

from product.models import CustomerProduct, Product,ProductMultiprice, ProductCategory
from rest_framework.viewsets import ModelViewSet

class ProductMultipriceapi(ListAPIView):
    def get(self, request):
        try:
            products_list = Product.objects.all().values(
        "id",
        "title",
        "slug",
        "description",
        "image",
        "price",
        "is_taxable",
        "product_id",
        "unit",
        "category",
        "barcode"
        )
            temp_data = products_list
            for index,item in enumerate(products_list):
                print(item["id"])
                queryset = ProductMultiprice.objects.filter(product_id=item["id"]).values()
                temp_data[index]["multiprice"]=queryset
            return Response(temp_data,200)

        except Exception as error:
            return Response({"message":str(error)})


class ProductTypeListView(ListAPIView):
    serializer_class = ProductCategorySerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
       
        products = Product.objects.all()

        item_type ={
            "FOOD":{
                "title":"FOOD",
                "group": []
            },
            "BEVERAGE":{
                "title":"BEVERAGE",
                "group": []
            },
            "OTHERS": {
                "title":"OTHERS",
                "group": []
            }
        }
        type_group = {"FOOD": [],"BEVERAGE": [],"OTHERS": []}

        product_list = []

        for product in products:
            product_dict =  model_to_dict(product)
            del product_dict['image']
            product_dict['type'] = product.type.title
            product_list.append(product_dict)


        for product in product_list:
            if  product['group'] not in type_group[product['type']]:
                type_group[product['type']].append(product['group'])
                item_type[product['type']]['group'].append({"title":product['group'], "items":[]})
        
        for product in product_list:
            group_list = item_type[product['type']]['group']
            for i in group_list:
                if i['title'] == product['group']:
                    i['items'].append(product)



            
        return Response(item_type)

        


class ProductList(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = None

    def get_queryset(self):
        return Product.objects.active()
    
    


class ProductDetail(RetrieveAPIView):
    serializer_class = ProductSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return Product.objects.active()


class CustomerProductAPI(ModelViewSet):
    serializer_class = CustomerProductSerializer
    queryset = CustomerProduct.objects.active()

    def create(
        self,
        request,
        *args,
        **kwargs,
    ):

        is_added = CustomerProduct.objects.filter(
            is_deleted=False,
            status=True,
            customer=request.data["customer"],
            product=request.data["product"],
        )

        if not is_added:
            return super().create(request, *args, **kwargs)
        else:
            return Response(
                {"message": "This product is already added to the customer"},
            )

    def get_queryset(self, *args, **kwargs):
        customer_id = self.request.query_params.get("customerId")
        if customer_id:
            queryset = CustomerProduct.objects.filter(
                is_deleted=False, status=True, customer=customer_id
            )

            return queryset
        else:
            return super().get_queryset()

    def get_serializer_class(self):
        detail_actions = ["retrieve", "list"]
        if self.action in detail_actions:
            return CustomerProductDetailSerializer
        return super().get_serializer_class()
