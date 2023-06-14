from accounting.models import AccountLedger, TblCrJournalEntry, TblJournalEntry, TblDrJournalEntry, AccountChart, AccountSubLedger
from decimal import Decimal


def update_terminal_sub_ledger(terminal, branch, total, ledger):
    
    subled_name = f'{ledger.ledger_name} {branch}-{terminal}'
    try:
        sub = AccountSubLedger.objects.get(sub_ledger_name=subled_name)
        sub.total_value += Decimal(total)
        sub.save()

    except AccountSubLedger.DoesNotExist:
        AccountSubLedger.objects.create(sub_ledger_name=subled_name, total_value=total, is_editable=False, ledger=ledger)

def update_terminal_amount(terminal, branch, total):
    subled_name = f'Sales {branch}-{terminal}'
    sale_ledger = AccountLedger.objects.get(ledger_name='Sales')
    try:
        sub = AccountSubLedger.objects.get(sub_ledger_name=subled_name)
        sub.total_value += Decimal(total)
        sub.save()

    except AccountSubLedger.DoesNotExist:
        AccountSubLedger.objects.create(sub_ledger_name=subled_name, total_value=total, is_editable=False, ledger=sale_ledger)

def create_journal_for_complimentary(instance):
    grand_total = Decimal(instance.grand_total)
    complimentary_sales = AccountLedger.objects.get(ledger_name__iexact='complimentary sales')
    complimentary_expenses = AccountLedger.objects.get(ledger_name__iexact='complimentary expenses')

    journal_entry = TblJournalEntry.objects.create(employee_name='Created automatically during sale', journal_total=grand_total)
    TblDrJournalEntry.objects.create(particulars="Complimentary Expenses A/C Dr.", debit_amount = grand_total, journal_entry=journal_entry, ledger=complimentary_expenses)
    TblCrJournalEntry.objects.create(particulars="To Complimentary Sales", credit_amount = grand_total, journal_entry=journal_entry, ledger=complimentary_sales)
    
    complimentary_expenses.total_value += grand_total
    complimentary_expenses.save()

    complimentary_sales.total_value += grand_total
    complimentary_sales.save()


"""   :-(   """


def create_journal_for_bill(instance):
    payment_mode = instance.payment_mode.lower().strip()
    grand_total = Decimal(instance.grand_total)
    tax_amount = Decimal(instance.tax_amount)
    discount_amount = Decimal(instance.discount_amount)
    sale_ledger = AccountLedger.objects.get(ledger_name='Sales')


    if discount_amount > 0:
        discount_expenses = AccountLedger.objects.get(ledger_name__iexact='Discount Expenses')
        discount_sales = AccountLedger.objects.get(ledger_name__iexact='Discount Sales')

        journal_entry = TblJournalEntry.objects.create(employee_name='Created automatically during sale', journal_total=discount_amount)
        TblDrJournalEntry.objects.create(particulars="Complimentary Expenses A/C Dr.", debit_amount = discount_amount, journal_entry=journal_entry, ledger=discount_expenses)
        TblCrJournalEntry.objects.create(particulars="To Complimentary Sales", credit_amount = discount_amount, journal_entry=journal_entry, ledger=discount_sales)
        
        discount_expenses.total_value += discount_amount
        discount_expenses.save()

        discount_sales.total_value += discount_amount
        discount_sales.save()

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
        sale_ledger.total_value += (grand_total-tax_amount)
        sale_ledger.save()
        if tax_amount > 0:
            vat_payable = AccountLedger.objects.get(ledger_name='VAT Payable')
            vat_payable.total_value = vat_payable.total_value + tax_amount
            vat_payable.save()
            TblCrJournalEntry.objects.create(journal_entry=journal_entry, particulars=f"To VAT Payable", ledger=vat_payable, credit_amount=tax_amount)
        
    elif payment_mode == "credit card":
        card_transaction_ledger = AccountLedger.objects.get(ledger_name='Card Transactions')
        update_terminal_sub_ledger(terminal=instance.terminal, branch=instance.branch.branch_code, total=grand_total, ledger=card_transaction_ledger)

        journal_entry = TblJournalEntry.objects.create(employee_name='Created Automatically during Sale', journal_total=grand_total)
        TblDrJournalEntry.objects.create(journal_entry=journal_entry, particulars=f"Card Transaction A/C Dr", ledger=card_transaction_ledger, debit_amount=grand_total)
        TblCrJournalEntry.objects.create(journal_entry=journal_entry, particulars=f"To Sales", ledger=sale_ledger, credit_amount=grand_total)

        card_transaction_ledger.total_value += (grand_total-tax_amount)
        card_transaction_ledger.save()

        sale_ledger.total_value += grand_total
        sale_ledger.save()

        if tax_amount > 0:
            vat_payable = AccountLedger.objects.get(ledger_name='VAT Payable')
            vat_payable.total_value = vat_payable.total_value + tax_amount
            vat_payable.save()
            TblCrJournalEntry.objects.create(journal_entry=journal_entry, particulars=f"To VAT Payable", ledger=vat_payable, credit_amount=tax_amount)

    elif payment_mode == "mobile payment":
        mobile_payment = AccountLedger.objects.get(ledger_name='Mobile Payments')
        update_terminal_sub_ledger(terminal=instance.terminal, branch=instance.branch.branch_code, total=grand_total, ledger=mobile_payment)

        journal_entry = TblJournalEntry.objects.create(employee_name='Created Automatically during Sale', journal_total=grand_total)
        TblDrJournalEntry.objects.create(journal_entry=journal_entry, particulars=f"Mobile Payment A/C Dr", ledger=mobile_payment, debit_amount=grand_total)
        TblCrJournalEntry.objects.create(journal_entry=journal_entry, particulars=f"To Sales", ledger=sale_ledger, credit_amount=grand_total)
        mobile_payment.total_value += (grand_total-tax_amount)
        mobile_payment.save()

        sale_ledger.total_value += grand_total
        sale_ledger.save()

    elif payment_mode == "cash":
        cash_ledger = AccountLedger.objects.get(ledger_name='Cash-In-Hand')
        update_terminal_sub_ledger(terminal=instance.terminal, branch=instance.branch.branch_code, total=grand_total, ledger=cash_ledger)
        cash_ledger.total_value = cash_ledger.total_value + grand_total
        cash_ledger.save()

        sale_ledger.total_value = sale_ledger.total_value+(grand_total-tax_amount)
        sale_ledger.save()

        journal_entry = TblJournalEntry.objects.create(employee_name='Created Automatically during Sale', journal_total=grand_total)
        TblDrJournalEntry.objects.create(journal_entry=journal_entry, particulars=f"Cash A/C Dr", ledger=cash_ledger, debit_amount=grand_total)
        TblCrJournalEntry.objects.create(journal_entry=journal_entry, particulars=f"To Sales", ledger=sale_ledger, credit_amount=(grand_total-tax_amount))
        if tax_amount > 0:
            vat_payable = AccountLedger.objects.get(ledger_name='VAT Payable')
            vat_payable.total_value = vat_payable.total_value + tax_amount
            vat_payable.save()
            TblCrJournalEntry.objects.create(journal_entry=journal_entry, particulars=f"To VAT Payable", ledger=vat_payable, credit_amount=tax_amount)


def create_split_payment_accounting(payment, total, branch, terminal, tax_amount, customer, discount):
    discount_amount = Decimal(discount)
    sale_ledger = AccountLedger.objects.get(ledger_name='Sales')
    sale_ledger.total_value = sale_ledger.total_value+Decimal(total-tax_amount)
    sale_ledger.save()
    
    journal = TblJournalEntry.objects.create(employee_name='Created Automatically during Sale', journal_total=total)
    TblCrJournalEntry.objects.create(journal_entry=journal, particulars=f"To Sales", ledger=sale_ledger, credit_amount=(total-tax_amount))
    if tax_amount > 0:
            vat_payable = AccountLedger.objects.get(ledger_name='VAT Payable')
            vat_payable.total_value = vat_payable.total_value + Decimal(tax_amount)
            vat_payable.save()
            TblCrJournalEntry.objects.create(journal_entry=journal, particulars=f"To VAT Payable", ledger=vat_payable, credit_amount=tax_amount)
    if discount_amount > 0:
        discount_expenses = AccountLedger.objects.get(ledger_name__iexact='Discount Expenses')
        TblDrJournalEntry.objects.create(particulars="Discount Expenses A/C Dr.", debit_amount = discount_amount, journal_entry=journal, ledger=discount_expenses)
        discount_expenses.total_value += discount_amount
        discount_expenses.save()



    for pay in payment:
        pay_amount = Decimal(pay.get('amount'))
        if pay['payment_mode'].lower().strip() == "cash":
            cash_ledger = AccountLedger.objects.get(ledger_name='Cash-In-Hand')
            update_terminal_sub_ledger(terminal=terminal, branch=branch, total= pay_amount, ledger=cash_ledger)
            cash_ledger.total_value = cash_ledger.total_value + pay_amount
            cash_ledger.save()
            TblDrJournalEntry.objects.create(journal_entry=journal, particulars=f"Cash A/C Dr", ledger=cash_ledger, debit_amount=pay_amount)

        elif pay['payment_mode'].lower().strip() == "mobile payment":
            mobile_payment = AccountLedger.objects.get(ledger_name='Mobile Payments')
            update_terminal_sub_ledger(terminal=terminal, branch=branch, total= pay_amount, ledger=mobile_payment)
            mobile_payment.total_value += pay_amount
            mobile_payment.save()
            TblDrJournalEntry.objects.create(journal_entry=journal, particulars=f"Mobile Payment A/C Dr", ledger=mobile_payment, debit_amount=pay_amount)
        
        elif pay['payment_mode'].lower().strip() == "credit card":
            card_transaction_ledger = AccountLedger.objects.get(ledger_name='Card Transactions')
            update_terminal_sub_ledger(terminal=terminal, branch=branch, total= pay_amount, ledger=card_transaction_ledger)
            TblDrJournalEntry.objects.create(journal_entry=journal, particulars=f"Card Transaction A/C Dr", ledger=card_transaction_ledger, debit_amount=pay_amount)
            card_transaction_ledger.total_value += pay_amount
            card_transaction_ledger.save()

        elif pay['payment_mode'].lower().strip() == "credit": 
            account_chart = AccountChart.objects.get(group='Sundry Debtors')
            try:
                dr_ledger = AccountLedger.objects.get(ledger_name=f'{customer.pk} - {customer.name}')
                dr_ledger.total_value += pay_amount
                dr_ledger.save()
            except AccountLedger.DoesNotExist:
                dr_ledger = AccountLedger.objects.create(ledger_name=f'{customer.pk} - {customer.name}', account_chart=account_chart, total_value=pay_amount)
            TblDrJournalEntry.objects.create(journal_entry=journal, particulars=f"{customer.name} A/C Dr", ledger=dr_ledger, debit_amount=pay_amount)



def reverse_accounting(instance):
    pass