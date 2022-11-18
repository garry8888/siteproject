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

    return cur_id


def country(iso):
    try:
        id = Countries.objects.get(abbreviation=iso).id

    except ObjectDoesNotExist:
        id = None

    return id


# BNP Paribas Bank: get merchant from rough bank statement data
def get_merchant(transaction_details):

    if len(transaction_details) == 2 or len(transaction_details) == 3:
        raw_merchant_data = transaction_details[1].lstrip().split(' ')
        del raw_merchant_data[0]
        merchant_data = ' '.join(raw_merchant_data)

    else:
        merchant_data = transaction_details[0]

    return merchant_data


# Alfa-Bank: retrieve and upload clear financial data for reports
def create_bank_statements(user_id, bank_id):
    data = check_last_update(user_id, bank_id)
    mcc_d = []

    def get_mcc(code):
        c = ''
        try:
            c = code.replace('MCC', '')
            merchant_code = c.replace(')', '')
        except IndexError or TypeError:
            merchant_code = 4829

        return merchant_code

    for row in data:
        purpose = row.purpose
        amount = row.amount
        # print(row.id, row.purpose, row.amount, row.date_operation)

        if purpose.startswith('Покупка') or purpose.startswith('Зняття') or purpose.startswith('Списание'):
            transaction = purpose.split(',')    # ['Покупка (EPICENTR KAFE(P0019265)', ' Kyiv', ' UKR', 'MCC 5812)']
            len_transaction = len(transaction) - 1
            mcc = get_mcc(transaction[len_transaction])

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


# BNP Paribas Bank: retrieve clear financial data for reports
def bnp_paribas_upload_clear_financial_data(user_id, bank_id):
    data = check_last_update(user_id, bank_id)
    clear_financial_data = []

    for item in data:
        purpose = item.purpose
        amount = item.amount
        transaction = purpose.split(' ')
        len_transaction = len(transaction) - 1

        clear_financial_data.append(dict(
            transaction_place=' '.join(transaction[:len_transaction]),
            type_expenses_id=12,
            # TODO adding new MCC to DB
            type_transaction_id=MoneyTransaction.objects.get(type_transaction_en=amount_transaction(amount)).id,
            sum_transaction=amount,
            currency_id=currency(transaction[len_transaction]),
            country_id=country(transaction[len_transaction]),
            date_of_trans=item.date_operation,
            user_id=user_id,
            bank_id=bank_id,
            original_id=item.id
        ))

    BankStatements.objects.bulk_create([BankStatements(**r) for r in clear_financial_data])
    print('BS LOAD', clear_financial_data)
