import camelot


# get data from pdf and delete head of the doc (not table data)
def get_pdf_data(pdf_file):
    try:
        tables = camelot.read_pdf(pdf_file, pages='all', flavor="stream", row_tol=15)
        list_data = []

        for table in tables:
            list_data.append(table.data)

        # удаляем лишние заголовки документа и ищем начало тела таблицы
        for data in list_data:
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
        return list_data

    except NotImplementedError:
        return 'Incorrect format'
