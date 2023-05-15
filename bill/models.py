from datetime import datetime
import black
from django.contrib.auth import get_user_model

from django.db import models
from django.dispatch import receiver
from django.forms import FloatField
from organization.models import Organization
from product.models import Product, ProductStock
from root.utils import BaseModel
from django.db.models.signals import post_save, pre_save
from .utils import create_journal_for_bill

User = get_user_model()


class TblTaxEntry(models.Model):
    idtbltaxEntry = models.AutoField(primary_key=True)
    fiscal_year = models.CharField(max_length=20)
    bill_no = models.CharField(null=True, max_length=20)
    customer_name = models.CharField(max_length=200, null=True)
    customer_pan = models.CharField(max_length=200, null=True)
    bill_date = models.DateField(null=True)
    amount = models.FloatField(null=True)
    discount = models.FloatField(null=True)
    taxable_amount = models.FloatField(null=True)
    tax_amount = models.FloatField(null=True)
    is_printed = models.CharField(max_length=20, default="Yes")
    is_active = models.CharField(max_length=20, default="Yes")
    printed_time = models.CharField(null=True, max_length=20)
    entered_by = models.CharField(null=True, max_length=20)
    printed_by = models.CharField(null=True, max_length=20)
    is_realtime = models.CharField(max_length=20, default="Yes")
    sync_with_ird = models.CharField(max_length=20, default="Yes")
    payment_method = models.CharField(null=True, max_length=20, default="Cash")
    vat_refund_amount = models.FloatField(default=0.0)
    transaction_id = models.CharField(null=True, max_length=20)
    unit = models.CharField(default="-", max_length=20)

    class Meta:
        db_table = "tbltaxentry"

    def __str__(self):
        return f"{self.idtbltaxEntry}- {self.fiscal_year} - {self.bill_no}"


class TblSalesEntry(models.Model):
    tblSalesEntry = models.AutoField(primary_key=True)
    bill_date = models.CharField(null=True, max_length=20)
    bill_no = models.CharField(null=True, max_length=20)
    customer_name = models.CharField(max_length=200, null=True)
    customer_pan = models.CharField(max_length=200, null=True)
    amount = models.FloatField(null=True, default=0.0)
    NoTaxSales = models.FloatField(default=0.0)
    ZeroTaxSales = models.FloatField(default=0.0)
    taxable_amount = models.FloatField(null=True, default=0.0)
    tax_amount = models.FloatField(null=True, default=0.0)
    miti = models.CharField(null=True, max_length=20)
    ServicedItem = models.CharField(max_length=20, default="Goods")
    quantity = models.PositiveIntegerField(default=1)
    exemptedSales = models.CharField(default="0", max_length=20)
    export = models.CharField(default="0", max_length=20)
    exportCountry = models.CharField(default="0", max_length=20)
    exportNumber = models.CharField(default="0", max_length=20)
    exportDate = models.CharField(default="0", max_length=20)
    unit = models.CharField(default="-", max_length=20)

    class Meta:
        db_table = "tblSalesEntry"

    def __str__(self):
        return f"{self.tblSalesEntry}- {self.bill_date} - {self.bill_no}"


class TablReturnEntry(models.Model):
    idtblreturnEntry = models.AutoField(primary_key=True)
    bill_date = models.CharField(null=True, max_length=20)
    bill_no = models.CharField(null=True, max_length=20)
    customer_name = models.CharField(max_length=200, null=True)
    customer_pan = models.CharField(max_length=200, null=True)
    amount = models.FloatField(null=True, default=0.0)
    NoTaxSales = models.FloatField(default=0.0)
    ZeroTaxSales = models.FloatField(default=0.0)
    taxable_amount = models.FloatField(null=True, default=0.0)
    tax_amount = models.FloatField(null=True, default=0.0)
    miti = models.CharField(null=True, max_length=20)
    ServicedItem = models.CharField(max_length=20, default="Goods")
    quantity = models.PositiveIntegerField(default=1)
    reason = models.TextField(null=True, blank=True)
    exemptedSales = models.CharField(default="0", max_length=20)
    export = models.CharField(default="0", max_length=20)
    exportCountry = models.CharField(default="0", max_length=20)
    exportNumber = models.CharField(default="0", max_length=20)
    exportDate = models.CharField(default="0", max_length=20)
    unit = models.CharField(default="-", max_length=20)

    class Meta:
        db_table = "tblreturnentry"

    def __str__(self):
        return f"{self.idtblreturnEntry}- {self.bill_date} - {self.bill_no}"


class PaymentType(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Payment Type Title")
    description = models.TextField(null=True, verbose_name="Payment Type Description")
    icon = models.ImageField(upload_to="payment-type/icons/", null=True, blank=True)
    slug = models.SlugField(unique=True, verbose_name="Payment Type Slug")

    def __str__(self):
        return self.title


class BillItem(BaseModel):
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product_title = models.CharField(
        max_length=255, verbose_name="Product Title", null=True
    )
    product_quantity = models.PositiveBigIntegerField(default=1)
    rate = models.FloatField(default=0.0)
    unit_title = models.CharField(max_length=50, null=True)
    amount = models.FloatField(
        default=0.0,
    )
    is_taxable = models.BooleanField(default=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    kot_id = models.IntegerField(null=True, blank=True)
    bot_id = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return f"{self.product_title}"

    # def save(self, *args, **kwrgs):
    #     try:
    #         print("-------------------------------")
    #         print("self product")
    #         print(self.new_product)
    #         if self.new_product:
    #             self.product_title = self.new_product.title
    #             self.unit_title = self.new_product.unit
    #             self.amount = self.product_quantity * self.rate
    #             super().save(*args, **kwrgs)
    #     except:
    #         pass


''' Signal for Decresing Product Stock after Sold '''

# def update_stock(sender, instance, **kwargs):
#     stock = ProductStock.objects.get(product=instance.product)
#     try:
#         stock.stock_quantity = stock.stock_quantity - int(instance.product_quantity)
#         stock.save()
#     except Exception as e:
#         print(e)
    

# post_save.connect(update_stock, sender=BillItem)

""" **************************************** """


class Bill(BaseModel):
    fiscal_year = models.CharField(max_length=20, null=True)
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    agent_name = models.CharField(max_length=255, null=True)
    terminal = models.CharField(max_length=10, default="1")
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    customer_address = models.CharField(max_length=255, null=True, blank=True)
    customer_tax_number = models.CharField(max_length=255, null=True, blank=True)
    customer = models.ForeignKey("user.Customer", on_delete=models.SET_NULL, null=True)
    transaction_date_time = models.DateTimeField(auto_now_add=True)
    transaction_date = models.DateField(auto_now_add=True)

    transaction_miti = models.CharField(max_length=255, null=True, blank=True)
    sub_total = models.FloatField(default=0.0)
    discount_amount = models.FloatField(default=0.0)
    taxable_amount = models.FloatField(default=0.0)
    tax_amount = models.FloatField(default=0.0)
    grand_total = models.FloatField(default=0.0)
    service_charge = models.FloatField(default=0.0)

    invoice_number = models.CharField(max_length=255, null=True, blank=True)
    amount_in_words = models.TextField(null=True, blank=True)
    payment_mode = models.CharField(
        max_length=255, default="Cash", blank=True, null=True
    )

    bill_items = models.ManyToManyField(BillItem, blank=False)
    organization = models.ForeignKey(
        "organization.Organization", on_delete=models.SET_NULL, null=True
    )
    branch = models.ForeignKey(
        "organization.Branch", on_delete=models.SET_NULL, null=True
    )
    print_count = models.PositiveIntegerField(default=1)
    # is_taxable = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.customer_name}-{self.transaction_date}- {self.grand_total}"


@receiver(post_save, sender=Bill)
def create_invoice_number(sender, instance, created, **kwargs):
    current_fiscal_year = Organization.objects.last().current_fiscal_year
    # terminal = "1"
    # if Bill.objects.all().count() >= 2:
    #     print("IF LEN 2 : ")
    #     current_fiscal_year_in_bill = (
    #         Bill.objects.all().order_by("pk").reverse()[1].fiscal_year
    #     )
    #     current_bill_number = (
    #         Bill.objects.all().order_by("pk").reverse()[1].invoice_number
    #     )
    # elif len(Bill.objects.all()) == 1:
    #     print("IF LEN == 1 : ")

    #     current_fiscal_year_in_bill = current_fiscal_year
    #     current_bill_number = "PW-0"

    # else:
    #     print("IF LEN else : ")

    #     current_fiscal_year_in_bill = current_fiscal_year
    #     current_bill_number = "PW-0"
    # print(
    #     "\n\n",
    #     f"Current Fiscal Year : {current_fiscal_year} \n Current Fiscal Year in Bill : {current_fiscal_year_in_bill} \n Current Bill Number : {current_bill_number}",
    # )

    if created:

        try:
            create_journal_for_bill(instance)
        except Exception as e:
            pass

        branch = instance.branch.branch_code
        terminal = instance.terminal
        branch_and_terminal = f"{branch}-{terminal}"

        bill_number = 0
        invoice_number = ""
        instance.fiscal_year = current_fiscal_year
        # if current_bill_number == None:
        #     bill_number = 1
        # else:
        last_bill_number = (
            Bill.objects.filter(invoice_number__startswith=branch_and_terminal)
            .order_by("pk")
            .reverse()
            .first()
        )
        if last_bill_number:
            current_bill_number_pk = last_bill_number.invoice_number.split("-")[-1]

            if current_bill_number_pk:
                bill_number = int(current_bill_number_pk) 
            else:
                bill_number = 1
            print(bill_number, "Incremented Bill Number")
        else:
            bill_number = 1

        if branch is not None:
            invoice_number = f"{branch}-{terminal}-{bill_number}"

        else:
            invoice_number = f"{terminal}-{bill_number}"

        instance.invoice_number = invoice_number

        a = TblTaxEntry(
            fiscal_year=current_fiscal_year,
            bill_no=invoice_number,
            customer_name=instance.customer_name,
            customer_pan=instance.customer_tax_number,
            bill_date=instance.transaction_date,
            amount=instance.grand_total,
            taxable_amount=instance.taxable_amount,
            tax_amount=instance.tax_amount,
            is_printed="Yes",
            printed_time=str(datetime.now().time().strftime(("%I:%M %p"))),
            entered_by=instance.agent_name,
            printed_by=instance.agent_name,
            is_realtime="Yes",
            sync_with_ird="Yes",
            payment_method=instance.payment_mode,
            vat_refund_amount=0.0,
            transaction_id="-",
        )

        b = TblSalesEntry(
            bill_date=instance.transaction_date,
            customer_name=instance.customer_name,
            customer_pan=instance.customer_tax_number,
            amount=instance.grand_total,
            NoTaxSales=0.0,
            ZeroTaxSales=0.0,
            taxable_amount=instance.taxable_amount,
            tax_amount=instance.tax_amount,
            miti=instance.transaction_miti,
            ServicedItem="Goods",
            quantity=1.0,
            bill_no=invoice_number,
        )

        if instance.tax_amount == 0:
            a.exemptedSales = instance.sub_total
            b.exemptedSales = instance.sub_total

        b.save()

        a.save()
        instance.save()


class BillItemVoid(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    bill_item = models.ForeignKey(BillItem, on_delete=models.CASCADE, default=1)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.product.title} void by quantity -> {self.quantity}'


class BillPayment(BaseModel):
    bill = models.ForeignKey(Bill, on_delete=models.PROTECT)
    payment_mode = models.CharField(max_length=100)
    rrn = models.CharField(max_length=100, null=True, blank=True)
    amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __str__(self):
        return self.payment_mode


