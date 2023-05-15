from django.db import models
from root.utils import BaseModel, SingletonModel


class StaticPage(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    published_date = models.DateField(null=True, blank=True)
    keywords = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Organization(SingletonModel, BaseModel):
    # basic company details
    org_name = models.CharField(max_length=255)
    org_logo = models.ImageField(
        upload_to="organization/images/", null=True, blank=True
    )
    tax_number = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="PAN/VAT Number"
    )
    website = models.URLField(null=True, blank=True)
    current_fiscal_year = models.CharField(null=True, max_length=20)
    start_year = models.IntegerField()
    end_year = models.IntegerField()

    # contact details
    company_contact_number = models.CharField(max_length=255, null=True, blank=True)
    company_contact_email = models.EmailField(null=True, blank=True)
    contact_person_name = models.CharField(max_length=255, null=True, blank=True)
    contact_person_number = models.CharField(max_length=255, null=True, blank=True)
    company_address = models.CharField(max_length=255, null=True, blank=True)
    company_bank_qr = models.ImageField(
        upload_to="organization/images/", null=True, blank=True
    )

    def __str__(self):
        return self.org_name
    
    def get_fiscal_year(self):
        return f'{self.start_year}-{self.end_year}'


import shortuuid
import six

from uuid import uuid4


def get_default_uuid():
    return uuid4().hex


class Branch(BaseModel):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    contact_number = models.CharField(max_length=50, null=True, blank=True)
    branch_manager = models.CharField(max_length=255, null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    branch_code = models.CharField(
        max_length=255, null=False, blank=False, unique=True, default=get_default_uuid
    )

    def __str__(self):
        return f"{self.organization.org_name} - {self.name}"



class Terminal(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    terminal_no = models.PositiveIntegerField()

    def __str__(self):
        return f'Terminal {self.terminal_no} of branch {self.branch.name}'
    


class PrinterSetting(BaseModel):

    PRINTER_LOCATION = (
        ('KITCHEN', "KITCHEN"),
        ("BAR", "BAR")
    )

    terminal = models.ForeignKey(Terminal, on_delete=models.CASCADE)
    url = models.CharField(max_length=100, null=True, blank=True)
    port = models.IntegerField(null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    printer_location = models.CharField(max_length=10, choices=PRINTER_LOCATION)

    def __str__(self):
        return f'Printer for terminal {self.terminal.terminal_no}'
    
    class Meta:
        unique_together = 'printer_location', 'terminal',



class Table(BaseModel):
    terminal = models.ForeignKey(Terminal, on_delete=models.CASCADE)
    table_number = models.CharField(max_length=10)
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.table_number} table from Terminal {self.terminal.terminal_no}'