from accounting.models import AccountLedger, TblCrJournalEntry, TblJournalEntry, TblDrJournalEntry, AccountChart
from decimal import Decimal

def create_journal_for_bill(instance):
    payment_mode = instance.payment_mode.lower()
    grand_total = Decimal(instance.grand_total)
    tax_amount = Decimal(instance.tax_amount)
    sale_ledger = AccountLedger.objects.get(ledger_name='Sales')

    if payment_mode == 'credit':
        account_chart = AccountChart.objects.get(group='Sundry Debtors')
        
        try:
            dr_ledger = AccountLedger.objects.get(ledger_name=f'{instance.customer.pk} - {instance.customer.name}')
            dr_ledger.total_value += grand_total
            dr_ledger.save()
        except AccountLedger.DoesNotExist:
            dr_ledger = AccountLedger.objects.create(ledger_name=f'{instance.customer.pk} - {instance.customer.name}', account_chart=account_chart, total_value=grand_total)

        journal_entry = TblJournalEntry.objects.create(employee_name='Created Automatically during Sale', journal_total=grand_total)
        TblDrJournalEntry.objects.create(journal_entry=journal_entry, particulars=f"{instance.customer.name} A/C Dr", ledger=dr_ledger, debit_amount=grand_total)
        TblCrJournalEntry.objects.create(journal_entry=journal_entry, particulars=f"To Sales", ledger=sale_ledger, credit_amount=(grand_total-tax_amount))
        if tax_amount > 0:
            vat_payable = AccountLedger.objects.get(ledger_name='VAT Payable')
            vat_payable.total_value = vat_payable.total_value + tax_amount
            vat_payable.save()
            TblCrJournalEntry.objects.create(journal_entry=journal_entry, particulars=f"To Vat Payable", ledger=vat_payable, credit_amount=tax_amount)
        
    elif payment_mode == "credit card":
        card_transaction_ledger = AccountLedger.objects.get(ledger_name='Card Transactions')

        journal_entry = TblJournalEntry.objects.create(employee_name='Created Automatically during Sale', journal_total=grand_total)
        TblDrJournalEntry.objects.create(journal_entry=journal_entry, particulars=f"Card Transaction A/C Dr", ledger=card_transaction_ledger, debit_amount=grand_total)
        TblCrJournalEntry.objects.create(journal_entry=journal_entry, particulars=f"To Sales", ledger=sale_ledger, credit_amount=grand_total)

        card_transaction_ledger.total_value += grand_total
        card_transaction_ledger.save()

        sale_ledger.total_value += grand_total
        sale_ledger.save()

    elif payment_mode == "mobile payment":
        mobile_payment = AccountLedger.objects.get(ledger_name='Mobile Payments')

        journal_entry = TblJournalEntry.objects.create(employee_name='Created Automatically during Sale', journal_total=grand_total)
        TblDrJournalEntry.objects.create(journal_entry=journal_entry, particulars=f"Mobile Payment A/C Dr", ledger=mobile_payment, debit_amount=grand_total)
        TblCrJournalEntry.objects.create(journal_entry=journal_entry, particulars=f"To Sales", ledger=sale_ledger, credit_amount=grand_total)

        mobile_payment.total_value += grand_total
        mobile_payment.save()

        sale_ledger.total_value += grand_total
        sale_ledger.save()

    else:
        
        cash_ledger = AccountLedger.objects.get(ledger_name='Cash-In-Hand')
        cash_ledger.total_value = cash_ledger.total_value + grand_total
        cash_ledger.save()

        sale_ledger.total_value = sale_ledger.total_value+(grand_total-tax_amount)
        sale_ledger.save()

        vat_payable = AccountLedger.objects.get(ledger_name='VAT Payable')
        vat_payable.total_value = vat_payable.total_value + tax_amount
        vat_payable.save()

        journal_entry = TblJournalEntry.objects.create(employee_name='Created Automatically during Sale', journal_total=grand_total)
        TblDrJournalEntry.objects.create(journal_entry=journal_entry, particulars=f"Cash A/C Dr", ledger=cash_ledger, debit_amount=grand_total)
        TblCrJournalEntry.objects.create(journal_entry=journal_entry, particulars=f"To Sales", ledger=sale_ledger, credit_amount=(grand_total-tax_amount))
        if tax_amount > 0:
            TblCrJournalEntry.objects.create(journal_entry=journal_entry, particulars=f"To Vat Payable", ledger=vat_payable, credit_amount=tax_amount)




    

