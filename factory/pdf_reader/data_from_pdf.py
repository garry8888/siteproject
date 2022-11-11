import camelot


# get rough data from pdf bank statement
def get_pdf_data(pdf_file):
    try:
        tables = camelot.read_pdf(pdf_file, pages='all', flavor="stream", row_tol=15)
        list_data = []

        for table in tables:
            list_data.append(table.data)

        return list_data

    except NotImplementedError:
        return 'Incorrect format'


# Alfa-bank: remove unnecessary document headers and look for the beginning of the table body
def alfa_bank_delete_headers(pdf_data):
    rough_pdf_data = pdf_data

    for data in rough_pdf_data:
        try:
            len_data = len(data[0])

            while len(data) != 0:
                if data[0][0] != 'Дата та час' or data[0][len_data - 1] == 'null':
                    del data[0]
                else:
                    break
            else:
                continue

        except IndexError:
            return 'Incorrect format'

    return rough_pdf_data


# BNP Paribas bank: remove unnecessary document headers/footers and look for the beginning of the table body
def bnp_paribas_delete_headers(pdf_data):
    rough_pdf_data = pdf_data[1:-1]
    rough_finance_data = []
    finance_data = []

    for data in rough_pdf_data:
        rough_finance_data.append(data[1:])

    for item in rough_finance_data:
        try:

            while len(item) != 0:
                finance_data.append(item[:2])

                if item[3][0] != '':
                    del item[:3]
                else:
                    del item[:4]

            else:
                continue

        except IndexError:
            pass

    return finance_data
