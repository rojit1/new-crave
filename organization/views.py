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
from user.models import Customer, User
from user.permission import IsAdminMixin

from .forms import OrganizationForm, StaticPageForm
from .models import Organization, StaticPage


class IndexView(IsAdminMixin, TemplateView):
    template_name = "index.html"


class OrganizationMixin(IsAdminMixin):
    model = Organization
    form_class = OrganizationForm
    paginate_by = 50
    queryset = Organization.objects.filter(status=True, is_deleted=False)
    success_url = reverse_lazy("org:organization_detail")


class OrganizationDetail(OrganizationMixin, DetailView):
    template_name = "organization/organization_detail.html"

    def get_object(self):
        return Organization.objects.last()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.all()
        branches = Branch.objects.filter(
            is_deleted=False, organization=self.get_object().id
        )
        customers = Customer.objects.filter(is_deleted=False)
        context["branches"] = branches
        context["customers"] = customers
        context["users"] = users

        return context


class OrganizationCreate(OrganizationMixin, CreateView):
    template_name = "create.html"


class OrganizationUpdate(OrganizationMixin, UpdateView):
    template_name = "update.html"

    def get_object(self):
        return Organization.objects.last()


class OrganizationDelete(OrganizationMixin, DeleteMixin, View):
    pass


class StaticPageMixin(IsAdminMixin):
    model = StaticPage
    form_class = StaticPageForm
    paginate_by = 50
    queryset = StaticPage.objects.filter(status=True, is_deleted=False)
    success_url = reverse_lazy("org:staticpage_list")
    search_lookup_fields = ["name", "content", "slug", "keywords"]


class StaticPageList(StaticPageMixin, ListView):
    template_name = "staticpage/staticpage_list.html"
    queryset = StaticPage.objects.filter(status=True, is_deleted=False)


class StaticPageDetail(StaticPageMixin, DetailView):
    template_name = "staticpage/staticpage_detail.html"


class StaticPageCreate(StaticPageMixin, CreateView):
    template_name = "create.html"


class StaticPageUpdate(StaticPageMixin, UpdateView):
    template_name = "update.html"


class StaticPageDelete(StaticPageMixin, DeleteMixin, View):
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
from .models import Branch
from .forms import BranchForm


class BranchMixin(IsAdminMixin):
    model = Branch
    form_class = BranchForm
    paginate_by = 50
    queryset = Branch.objects.filter(status=True, is_deleted=False)
    success_url = reverse_lazy("org:branch_list")
    search_lookup_fields = ["name", "address", "contact_number", "branch_manager"]


class BranchList(BranchMixin, ListView):
    template_name = "branch/branch_list.html"
    queryset = Branch.objects.filter(status=True, is_deleted=False)


class BranchDetail(BranchMixin, DetailView):
    template_name = "branch/branch_detail.html"


class BranchCreate(BranchMixin, CreateView):
    template_name = "create.html"

    def form_valid(self, form):
        form.instance.organization = self.request.user.organization
        return super().form_valid(form)


class BranchUpdate(BranchMixin, UpdateView):
    template_name = "update.html"


class BranchDelete(BranchMixin, DeleteMixin, View):
    pass


from .models import Terminal
from .forms import TerminalForm
class TerminalMixin:
    model = Terminal
    form_class = TerminalForm
    paginate_by = 10
    queryset = Terminal.objects.filter(status=True,is_deleted=False)
    success_url = reverse_lazy('org:terminal_list')

class TerminalList(TerminalMixin, ListView):
    template_name = "terminal/terminal_list.html"
    queryset = Terminal.objects.filter(status=True,is_deleted=False)

class TerminalDetail(TerminalMixin, DetailView):
    pass
    # template_name = "terminal/terminal_detail.html"

class TerminalCreate(TerminalMixin, CreateView):
    template_name = "create.html"

class TerminalUpdate(TerminalMixin, UpdateView):
    template_name = "update.html"

class TerminalDelete(TerminalMixin, DeleteMixin, View):
    pass


from .models import Table
from .forms import TableForm
class TableMixin:
    model = Table
    form_class = TableForm
    paginate_by = 10
    queryset = Table.objects.filter(status=True,is_deleted=False)
    success_url = reverse_lazy('org:table_list')

class TableList(TableMixin, ListView):
    template_name = "table/table_list.html"
    queryset = Table.objects.filter(status=True,is_deleted=False)

class TableDetail(TableMixin, DetailView):
    template_name = "table/table_detail.html"

class TableCreate(TableMixin, CreateView):
    template_name = "create.html"

class TableUpdate(TableMixin, UpdateView):
    template_name = "update.html"

class TableDelete(TableMixin, DeleteMixin, View):
    pass


from .models import PrinterSetting
from .forms import PrinterSettingForm
class PrinterSettingMixin:
    model = PrinterSetting
    form_class = PrinterSettingForm
    paginate_by = 10
    queryset = PrinterSetting.objects.filter(status=True,is_deleted=False)
    success_url = reverse_lazy('org:printersetting_list')

class PrinterSettingList(PrinterSettingMixin, ListView):
    template_name = "printersetting/printersetting_list.html"
    queryset = PrinterSetting.objects.filter(status=True,is_deleted=False)

class PrinterSettingDetail(PrinterSettingMixin, DetailView):
    template_name = "printersetting/printersetting_detail.html"

class PrinterSettingCreate(PrinterSettingMixin, CreateView):
    template_name = "create.html"

class PrinterSettingUpdate(PrinterSettingMixin, UpdateView):
    template_name = "update.html"

class PrinterSettingDelete(PrinterSettingMixin, DeleteMixin, View):
    pass

