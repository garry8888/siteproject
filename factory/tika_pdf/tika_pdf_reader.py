import tika
tika.initVM()
from tika import parser


def pdf_reader():
    raw_text = parser.from_file('C:\Users\Антон\Desktop\statement_7022035.pdf')
    raw_list = raw_text['content'].splitlines()
    return print(raw_list)
