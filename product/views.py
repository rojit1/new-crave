from django.shortcuts import redirect
from openpyxl import load_workbook

from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    View,
)
from root.utils import DeleteMixin
from user.permission import IsAdminMixin
from .models import ProductCategory
from .forms import ProductCategoryForm


class ProductCategoryMixin(IsAdminMixin):
    model = ProductCategory
    form_class = ProductCategoryForm
    paginate_by = 50
    queryset = ProductCategory.objects.filter(status=True, is_deleted=False)
    success_url = reverse_lazy("product_category_list")
    search_lookup_fields = [
        "title",
        "description",
    ]


class ProductCategoryList(ProductCategoryMixin, ListView):
    template_name = "productcategory/productcategory_list.html"
    queryset = ProductCategory.objects.filter(status=True, is_deleted=False)


class ProductCategoryDetail(ProductCategoryMixin, DetailView):
    template_name = "productcategory/productcategory_detail.html"


class ProductCategoryCreate(ProductCategoryMixin, CreateView):
    template_name = "create.html"


class ProductCategoryUpdate(ProductCategoryMixin, UpdateView):
    template_name = "update.html"


class ProductCategoryDelete(ProductCategoryMixin, DeleteMixin, View):
    pass


from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)
from root.utils import DeleteMixin
from .models import Product
from .forms import ProductForm


class ProductMixin(IsAdminMixin):
    model = Product
    form_class = ProductForm
    paginate_by = 50
    queryset = Product.objects.filter(status=True, is_deleted=False)
    success_url = reverse_lazy("product_list")
    search_lookup_fields = [
        "title",
        "description",
    ]


class ProductList(ProductMixin, ListView):
    template_name = "product/product_list.html"
    queryset = Product.objects.filter(status=True, is_deleted=False)


class ProductDetail(ProductMixin, DetailView):
    template_name = "product/product_detail.html"


class ProductCreate(ProductMixin, CreateView):
    template_name = "product/product_create.html"


class ProductUpdate(ProductMixin, UpdateView):
    template_name = "update.html"


class ProductDelete(ProductMixin, DeleteMixin, View):
    pass

class ProductUploadView(View):

    def post(self, request):
        file = request.FILES['file']
        wb = load_workbook(file)
        food_category, _ = ProductCategory.objects.get_or_create(title='FOOD')
        beverage_category, _ = ProductCategory.objects.get_or_create(title='BEVERAGE')
        others_category, _ = ProductCategory.objects.get_or_create(title='OTHERS')
        excel_data = list()
        for sheet in wb.worksheets:
            for row in sheet.iter_rows():
                row_data = list()
                for cell in row:
                    row_data.append(str(cell.value))
                row_data.insert(0, sheet.title)
                excel_data.append(row_data)
        for data in excel_data:
            if data[1].lower() == 'group':
                continue
            try:
                product = Product.objects.get(title__iexact=data[2])
                print(product)
                product.group = data[1]
                product.price = data[3]
                product.unit = data[4]
                product.is_taxable = True if data[5].lower() == "yes" else False
                product.is_produced = True if data[6].lower() == "yes" else False
                if "food" in data[0].lower():
                    product.type = food_category
                elif "beverage" in data[0].lower():
                    product.type = beverage_category
                else:
                    product.type = others_category
                product.save()
            except Product.DoesNotExist:
                pass
                product = Product()
                product.group = data[1]
                product.title=data[2]
                product.price = data[3]
                product.unit = data[4]
                product.is_taxable = True if data[5].lower() == "yes" else False
                product.is_produced = True if data[6].lower() == "yes" else False
                if "food" in data[0].lower():
                    product.type = food_category
                elif "beverage" in data[0].lower():
                    product.type = beverage_category
                else:
                    product.type = others_category
                product.save()

        return redirect(reverse_lazy("product_list"))

from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)
from root.utils import DeleteMixin
from .models import CustomerProduct
from .forms import CustomerProductForm


class CustomerProductMixin(IsAdminMixin):
    model = CustomerProduct
    form_class = CustomerProductForm
    paginate_by = 50
    queryset = CustomerProduct.objects.filter(status=True, is_deleted=False)
    success_url = reverse_lazy("customerproduct_list")
    search_lookup_fields = ["product__title", "customer__name", "agent__full_name"]


class CustomerProductList(CustomerProductMixin, ListView):
    template_name = "customerproduct/customerproduct_list.html"
    queryset = CustomerProduct.objects.filter(status=True, is_deleted=False)


class CustomerProductDetail(CustomerProductMixin, DetailView):
    template_name = "customerproduct/customerproduct_detail.html"


class CustomerProductCreate(CustomerProductMixin, CreateView):
    template_name = "create.html"

    def form_valid(self, form):
        form.instance.agent = self.request.user
        return super().form_valid(form)


class CustomerProductUpdate(CustomerProductMixin, UpdateView):
    template_name = "update.html"

    def form_valid(self, form):
        form.instance.agent = self.request.user
        return super().form_valid(form)


class CustomerProductDelete(CustomerProductMixin, DeleteMixin, View):
    pass

'''  STock VIews '''

from .models import ProductStock
from .forms import ProductStockForm

class ProductStockMixin:
    model = ProductStock
    form_class = ProductStockForm
    paginate_by = 10
    queryset = ProductStock.objects.filter(status=True,is_deleted=False)
    success_url = reverse_lazy('productstock_list')


class ProductStockList(ProductStockMixin, ListView):
    template_name = "productstock/productstock_list.html"
    queryset = ProductStock.objects.filter(status=True,is_deleted=False)

class ProductStockDetail(ProductStockMixin, DetailView):
    template_name = "productstock/productstock_detail.html"

class ProductStockCreate(ProductStockMixin, CreateView):
    template_name = "create.html"

class ProductStockUpdate(ProductStockMixin, UpdateView):
    template_name = "update.html"

class ProductStockDelete(ProductStockMixin, DeleteMixin, View):
    pass

"""  ----------------   """
from .models import BranchStock
from .forms import BranchStockForm
class BranchStockMixin:
    model = BranchStock
    form_class = BranchStockForm
    paginate_by = 10
    queryset = BranchStock.objects.filter(status=True,is_deleted=False)
    success_url = reverse_lazy('branchstock_list')

class BranchStockList(BranchStockMixin, ListView):
    template_name = "branchstock/branchstock_list.html"
    queryset = BranchStock.objects.filter(status=True,is_deleted=False)

class BranchStockDetail(BranchStockMixin, DetailView):
    template_name = "branchstock/branchstock_detail.html"

class BranchStockCreate(BranchStockMixin, CreateView):
    template_name = "create.html"

class BranchStockUpdate(BranchStockMixin, UpdateView):
    template_name = "update.html"

class BranchStockDelete(BranchStockMixin, DeleteMixin, View):
    pass