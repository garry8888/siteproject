import camelot


# get data from pdf and delete head of the doc (not table data)
def get_pdf_data(pdf_file):
    tables = camelot.read_pdf(pdf_file, pages='all', flavor="stream", row_tol=15)
    list_data = []
    for table in tables:
        list_data.append(table.data)

    for data in list_data:
        while data[0][0] != 'Дата та час' or data[0][4] == 'null':
            del data[0]
        else:
            break

    return list_data
