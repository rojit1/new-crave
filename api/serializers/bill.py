from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from bill.forms import TblTaxEntryForm
from bill.models import (
    Bill,
    BillItem,
    BillItemVoid,
    PaymentType,
    TablReturnEntry,
    TblSalesEntry,
    TblTaxEntry,
    BillPayment
)
from product.models import Product
from organization.models import Organization


class PaymentTypeSerializer(ModelSerializer):
    class Meta:
        model = PaymentType
        fields = ["id", "title"]


class BillItemSerializer(ModelSerializer):
    item_void_key = serializers.IntegerField(required=False)
    class Meta:
        model = BillItem
        fields = [
            "product_quantity",
            "product",
            "rate",
            "amount",
            "kot_id",
            "bot_id",
            "item_void_key"
        ]

class BillItemVoidSerializer(ModelSerializer):
    item_void_key = serializers.IntegerField()
    class Meta:
        model = BillItemVoid
        fields = ["product", "quantity", "bill_item", "item_void_key"]


class BillPaymentSerializer(ModelSerializer):
    class Meta:
        model = BillPayment
        fields = ['payment_mode', 'rrn', 'amount']


class BillSerializer(ModelSerializer):
    bill_items = BillItemSerializer(many=True)
    agent = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    items_void = BillItemVoidSerializer(many=True, required=False)
    split_payment = BillPaymentSerializer(many=True, write_only=True)

    class Meta:
        model = Bill
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured",
            "organization",
        ]
        optional_fields = [
            "fiscal_year",
            "invoice_number",
        ]

    def create(self, validated_data):
        bill_items = []
        items_data = validated_data.pop("bill_items")
        items_void = validated_data.pop("items_void")
        split_payment = validated_data.pop("split_payment")

        

        bill = Bill.objects.create(
            **validated_data, organization=Organization.objects.last()
        )

        for payment in split_payment:
            BillPayment.objects.create(bill=bill, payment_mode=payment['payment_mode'], rrn=payment['rrn'], amount=payment['amount'])


        for item in items_data:

            bill_item = BillItem.objects.create(
                product_quantity=item["product_quantity"],
                rate=item["rate"],
                product_title=item["product"].title,
                unit_title=item["product"].unit,
                amount=item["product_quantity"] * item["rate"],
                kot_id = item.get('kot_id', 0),
                bot_id = item.get('bot_id', 0),
            )

            item_void_key = item.get('item_void_key')
            for void_item in items_void:
                if void_item['item_void_key'] == item_void_key:
                    BillItemVoid.objects.create(product=void_item['product'], bill_item=bill_item, quantity=void_item['quantity'] )

            bill_items.append(bill_item)
        bill.bill_items.add(*bill_items)
        
        return bill


class BillDetailSerializer(ModelSerializer):
    bill_items = BillItemSerializer(many=True)
    agent = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Bill
        fields = "__all__"


class TblTaxEntrySerializer(ModelSerializer):
    reason = serializers.CharField(required=False)

    class Meta:
        model = TblTaxEntry
        fields = "__all__"

    def update(self, instance, validated_data):
        is_active_data = validated_data.get("is_active")
        reason = validated_data.get("reason")
        print("/n/n")
        print(instance.bill_no)
        print(instance.customer_pan)

        if is_active_data == "no":
            miti = ""
            quantity = 1
            try:
                print("TRY VITRA XU MA\n\n")
                obj = TblSalesEntry.objects.get(
                    bill_no=instance.bill_no, customer_pan=instance.customer_pan
                )
                print(obj)

                obj = Bill.objects.get(
                    invoice_number=instance.bill_no,
                    customer_tax_number=instance.customer_pan,
                )
                obj.status = False
                obj.save()
                # obj.save()

                print(obj)
                miti = obj.transaction_miti
                quantity = obj.bill_items.count()

                return_entry = TablReturnEntry(
                    bill_date=instance.bill_date,
                    bill_no=instance.bill_no,
                    customer_name=instance.customer_name,
                    customer_pan=instance.customer_pan,
                    amount=instance.amount,
                    NoTaxSales=0,
                    ZeroTaxSales=0,
                    taxable_amount=instance.taxable_amount,
                    tax_amount=instance.tax_amount,
                    miti=miti,
                    ServicedItem="Goods",
                    quantity=quantity,
                    reason=reason,
                )
                print(return_entry)
                return_entry.save()

            except:
                print("exception")
        instance.save()

        return super().update(instance, validated_data)


class TblTaxEntryVoidSerializer(ModelSerializer):
    reason = serializers.CharField(required=False)
    trans_date = serializers.CharField(required=True)
    class Meta:
        model = TblTaxEntry
        exclude = 'fiscal_year',

class TblSalesEntrySerializer(ModelSerializer):
    class Meta:
        model = TblSalesEntry
        fields = "__all__"


class TablReturnEntrySerializer(ModelSerializer):
    class Meta:
        model = TablReturnEntry
        fields = "__all__"
