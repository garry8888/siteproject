from datetime import datetime
from decimal import Decimal, InvalidOperation, DecimalException
from django.core.exceptions import ObjectDoesNotExist
from factory.models import BankStatementsData
from factory.pdf_reader.data_from_pdf import alfa_bank_delete_headers, get_pdf_data


# Alfa-bank: elimination of duplicates, checking the last date of the updated statement
def check_last_update(new_data):
    data = new_data[0]
    new_date = data['date_operation']
    new_amount = data['amount']
    user = data['user_id']
    try:
        exclude_duplicates = BankStatementsData.objects.\
            get(date_operation=new_date.date(), user=user, amount=new_amount)
    except ObjectDoesNotExist:
        exclude_duplicates = 0

    return exclude_duplicates


def load_bank_statement(pdf_file, user_id):
    new_rough_data = get_pdf_data(pdf_file)
    print('load', new_rough_data)
    new_data = alfa_bank_delete_headers(new_rough_data)

    if new_data == 'Incorrect format':
        return 0

    def numbers(num):
        try:
            if type(num) == int:
                nums = Decimal(num)
                return nums
            if type(num) == str:
                # убирает пробелы из числа: 1 000 000, замена , на .
                nums = Decimal(num.replace(' ', '').replace(',', '.'))
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
                # delete trash data (['00:00:00', '', '', 'MCC 6012)', '']) or (['ВСЬОГО:', '25 000,00', '27 507,20', '', ''])
                if i[count][2] == i[count][1] == '' or i[count][4] == i[count][3] == '':
                    del i[count]

                else:
                    d.append(dict(
                        purpose=i[count][3].replace('\n', ' '),
                        # if in data from bank statement Витрати -'' и 'Надходження' '', set 1
                        amount=numbers(i[count][2] if i[count][2] != '' else i[count][1] if i[count][1] != '' else 1),
                        date_operation=datetime.strptime(i[count][0].split()[0], "%d.%m.%Y"),
                        user_id=user_id
                    ))
                    count += 1

            except IndexError:
                break
        else:
            continue

    find_duplicates = check_last_update(d)

    if find_duplicates == 0:
        BankStatementsData.objects.bulk_create([BankStatementsData(**r) for r in d])
        print('LOAD')
    else:
        print('NOT LOAD')
        return 1

    return d
