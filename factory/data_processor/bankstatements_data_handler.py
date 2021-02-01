from django.contrib.auth.models import User

from factory.models import BankStatementsData, Mcc
from finance.models import Countries, MoneyTransaction, BankStatements
from django.core.exceptions import ObjectDoesNotExist



def create_bank_statements():
    data = BankStatementsData.objects.all()
    mcc_d = []

    def amount_transaction(transaction_sum):
        if transaction_sum < 0:
            type_t = 'rate'
        if transaction_sum > 0:
            type_t = 'replenishment'
        if transaction_sum == 0:
            pass
        return type_t

    def currency(iso):
        try:
            cur_id = Countries.objects.get(abbreviation=iso).currency_id
        except ObjectDoesNotExist:
            cur_id = None
            print('currency', iso)
        return cur_id

    def country(iso):
        try:
            id = Countries.objects.get(abbreviation=iso).id
        except ObjectDoesNotExist:
            id = None
            print('country', iso)
        return id

    def get_mcc(code):
        c = ''
        try:
            c = code.replace('MCC', '')
            merchant_code = c.replace(')', '')
        except IndexError or TypeError:
            merchant_code = 4829
            print('mcc', code)
        return merchant_code

    for row in data:
        purpose = row.purpose
        amount = row.amount

        if purpose.startswith('Покупка'):
            transaction = purpose.split(',')  # ['Покупка (EPICENTR KAFE(P0019265)', ' Kyiv', ' UKR', 'MCC 5812)']
            mcc = get_mcc(transaction[3])
            print(mcc, transaction)
            mcc_d.append(dict(
                transaction_place=transaction[0],
                type_expenses_id=Mcc.objects.get(mcc=mcc).type_expenses_id,
                type_transaction_id=MoneyTransaction.objects.get(type_transaction_en=amount_transaction(amount)).id,
                sum_transaction=amount,
                currency_id=currency(transaction[2].lstrip()),
                country_id=country(transaction[2].lstrip()),
                date_of_trans=row.date_operation,
                user_id=User.objects.get(id=row.user_id).id
            ))
        if not purpose.startswith('Покупка'):
            mcc_d.append(dict(
                transaction_place=purpose,
                type_expenses_id=12,
                type_transaction_id=MoneyTransaction.objects.get(type_transaction_en=amount_transaction(amount)).id,
                sum_transaction=amount,
                currency_id=None,
                country_id=None,
                date_of_trans=row.date_operation,
                user_id=User.objects.get(id=1).id
            ))

    BankStatements.objects.bulk_create([BankStatements(**r) for r in mcc_d])
