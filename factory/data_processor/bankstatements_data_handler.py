from factory.models import BankStatementsData, Mcc
from finance.models import Countries, MoneyTransaction, BankStatements
from django.core.exceptions import ObjectDoesNotExist


# checking the latest date of the uploaded statement in the DB for current user
def check_last_update(user, bank):
    try:
        last_transaction = BankStatements.objects.filter(user=user, bank=bank, original__isnull=False).\
            order_by('-date_of_trans')[0]
        exclude_duplicates = BankStatementsData.objects.filter(date_operation__gt=last_transaction.date_of_trans,
                                                               user=user, bank=bank)
    except IndexError:
        exclude_duplicates = BankStatementsData.objects.filter(user=user, bank=bank)

    return exclude_duplicates


def create_bank_statements(user_id, bank_id):
    data = check_last_update(user_id, bank_id)
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
            # print('country', iso)
        return id

    def get_mcc(code):
        c = ''
        try:
            c = code.replace('MCC', '')
            merchant_code = c.replace(')', '')
        except IndexError or TypeError:
            merchant_code = 4829
            # print('mcc', code)
        return merchant_code

    for row in data:
        purpose = row.purpose
        amount = row.amount
        # print(row.id, row.purpose, row.amount, row.date_operation)

        if purpose.startswith('Покупка') or purpose.startswith('Зняття') or purpose.startswith('Списание'):
            transaction = purpose.split(',')    # ['Покупка (EPICENTR KAFE(P0019265)', ' Kyiv', ' UKR', 'MCC 5812)']
            len_transaction = len(transaction) - 1
            mcc = get_mcc(transaction[len_transaction])
            print('---STRING 68', transaction, mcc)

            try:
                mcc_d.append(dict(
                    transaction_place=transaction[0],
                    type_expenses_id=Mcc.objects.get(mcc=mcc).type_expenses_id if mcc != '' else 12,  # TODO adding new MCC to DB
                    type_transaction_id=MoneyTransaction.objects.get(type_transaction_en=amount_transaction(amount)).id,
                    sum_transaction=amount,
                    currency_id=currency(transaction[2].lstrip()),
                    country_id=country(transaction[2].lstrip()),
                    date_of_trans=row.date_operation,
                    user_id=user_id,
                    bank_id=bank_id,
                    original_id=row.id
                ))

            except ObjectDoesNotExist:
                print('---STRING 90', transaction, mcc)
                mcc_d.append(dict(
                    transaction_place=transaction[0],
                    type_expenses_id=12,  # TODO adding new MCC to DB
                    type_transaction_id=MoneyTransaction.objects.get(type_transaction_en=amount_transaction(amount)).id,
                    sum_transaction=amount,
                    currency_id=currency(transaction[2].lstrip()),
                    country_id=country(transaction[2].lstrip()),
                    date_of_trans=row.date_operation,
                    user_id=user_id,
                    bank_id=bank_id,
                    original_id=row.id
                ))

        else:
            mcc_d.append(dict(
                transaction_place=purpose,
                type_expenses_id=12,
                type_transaction_id=MoneyTransaction.objects.get(type_transaction_en=amount_transaction(amount)).id,
                sum_transaction=amount,
                currency_id=None,
                country_id=None,
                date_of_trans=row.date_operation,
                user_id=user_id,
                bank_id=bank_id,
                original_id=row.id
            ))

    BankStatements.objects.bulk_create([BankStatements(**r) for r in mcc_d])
    print('BS LOAD', mcc_d)
