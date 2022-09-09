import xlrd
import xlwt
from xlwt import Workbook
from googletrans import Translator

translator =Translator()

location = (r'mvc.xlsx')

#Writing to file
wb_w = Workbook()
sheet1 = wb_w.add_sheet('sheet 1')
#Reading file
wb_r = xlrd.open_workbook(location)
sheet = wb_r.sheet_by_index(0)
sheet.cell_value(0,0)

#Going through each cell to translate and rewriting
for column in range(sheet.nrows):
    for row in range(sheet.ncols):
        print(sheet.cell_value(column, row))
        sheet1.write(column, row, translator.translate(sheet.cell_value(column, row), dest='en').text)

wb_w.save(r'test.xlsx')