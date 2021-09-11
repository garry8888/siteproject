from datetime import datetime, date
from decimal import Decimal, InvalidOperation, DecimalException
from django.core.exceptions import ObjectDoesNotExist
from factory.models import BankStatementsData
from factory.pdf_reader.data_from_pdf import get_pdf_data


# исключение дублей, проверка последней даты обновленной выписки
def check_last_update(new_data):
    data = new_data[0]
    new_date = data['date_operation']
    new_amount = data['amount']
    user = data['user_id']
    try:
        exclude_duplicates = BankStatementsData.objects.\
            get(date_operation=datetime.strptime(new_date, "%d.%m.%Y").date(), user=user, amount=new_amount)
    except ObjectDoesNotExist:
        exclude_duplicates = 0

    return exclude_duplicates


def load_bank_statement(new_data, user_id):

    def numbers(num):
        try:
            if type(num) == int:
                nums = Decimal(num)
                return nums
            if type(num) == str:
                nums = Decimal(num.replace(' ', '').replace(',', '.'))  # убирает пробелы из числа: 1 000 000, замена , на .
                return nums
            if type(num) == list:
                print('list', num)
                num = 0
                return num
        except InvalidOperation or DecimalException:
            print(num)
            nums_l = num.split('\n')
            print(nums_l)
            num_r = nums_l[0].replace(' ', '').replace(',', '.')
            print(num_r)
            nums = Decimal(num_r)
            return nums

    data = new_data
    d = []
    for i in data:
        len_data = len(i)
        count = 1
        while count < len_data:
            try:
                d.append(dict(
                    purpose=i[count][3].replace('\n', ' '),
                    amount=numbers(i[count][2] if i[count][2] != '' else 0),  # если Витрати -'', ставим 0
                    date_operation=i[count][0].split()[0],  # datetime.strptime(i[count][0].split()[0], "%d.%m.%Y").date()
                    user_id=user_id
                ))
                count += 1
            except IndexError:
                break
        else:
            continue

    find_duplicates = check_last_update(d)

    if find_duplicates == 0:
        #BankStatementsData.objects.bulk_create([BankStatementsData(**r) for r in d])
        #TODO django.core.exceptions.ValidationError: ['“31.08.2021” value has an invalid date format. It must be in YYYY-MM-DD format.']
        print('LOAD')
    else:
        print('NOT LOAD')
        return 1

    return d
