from xlsxwriter import Workbook
from datetime import datetime
from odbc import *
from SQLQueries import *
from io import BytesIO
# from info import data

def send_to_xlsx_fix(data, file_name="Reporte Especiales2 Contado"+ str(datetime.today()).replace(":","")+".xlsx", sheet_name="Especiales_2", headers=None):

    file_on_memory = BytesIO()

    workbook = Workbook(file_on_memory)
    worksheet = workbook.add_worksheet(sheet_name)
    date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})
    number_format = workbook.add_format({'num_format': '#,##0.00'})
    wrap_format = workbook.add_format({'text_wrap': 0})
    bold = workbook.add_format({'bold': 1})
    row, col = 1, 0

    # header_name = [column[0].replace("_", " ").upper() for column in data.description]

    options = {
        'name': 'Especiales_2',
        'total_row': True,
        'style': 'Table Style Medium 15',
        'columns': [
            {
             'header': 'NOMBRE', 'total_function': 'count',
             'format': bold,'header_format': wrap_format
            },
            {
             'header': ' ',
            },
            {
             'header': 'TOTAL SEMANA', 'total_function': 'sum', 'format':number_format, 'formula': '=SUM(Especiales_2[@[LUNES]:[SÁBADO]])'
            },
            {
             'header': 'LUNES', 'total_function': 'sum',
             'format': bold},
            {
             'header': 'MARTES', 'total_function': 'sum',
             'format': bold},
            {
             'header': 'MIÉRCOLES', 'total_function': 'sum',
             'format': bold},
            {
             'header': 'JUEVES', 'total_function': 'sum',
             'format': bold},
            {
             'header': 'VIERNES', 'total_function': 'sum',
             'format': bold},
            {
             'header': 'SÁBADO', 'total_function': 'sum',
             'format': bold},
            {
             'header': 'CLIENTE',
             'format': bold
            },
        ]}

    temp = []
    data_processed=[]
    duplicate_name=[]

    pos = 0
    index = 0

    for date,day_of_week,customer,name,amount,payment_method in data:
        name = (
            name.replace("TRAE","")
                .replace("CAJAS","")
                .replace("CAJA","")
                .replace("NO HIZO","")
                .replace("HIZO","")
                .replace("PEDIDOS","")
                .replace("PEDIDO","")
                .replace("SIN AZUCAR","")
                .replace("DOMOS","")
                .replace("DOMO","") 
                .replace("BANDEJAS","") 
                .replace("BANDEJA","")
                .replace("DMO MIXTO","")
                .replace("DMO MIXTA","")
                .replace("CASIT SURTI","")
                .replace(" CASIT ROSA","")
                .replace("  PARRILLA 2","")
                .replace(" CASIT 45 Y 20 AMARILLAS","")
            ).strip()
        if [name,date] not in temp:
            temp.append([name, date])
            data_processed.append([index,date,day_of_week,customer,name,str(amount),payment_method])
            index += 1
        elif [name,date] in temp:
            subindex = index-1
            data_processed[subindex][5] = '+'.join((str(data_processed[subindex][5]), str(amount)))


    index = 1
    for rowid, date,day_of_week,customer,name,amount,payment_method in data_processed:
        worksheet.write(index, 0, name)
        if name not in duplicate_name:
            duplicate_name.append(name)
            if day_of_week == 2:
                worksheet.write(index, 3, '='+amount)
            elif day_of_week == 3:
                worksheet.write(index, 4, '='+amount)
            elif day_of_week == 4:
                worksheet.write(index, 5, '='+amount)
            elif day_of_week == 5:
                worksheet.write(index, 6, '='+amount)
            elif day_of_week == 6:
                worksheet.write(index, 7, '='+amount)
            elif day_of_week == 7:
                worksheet.write(index, 8, '='+amount)
            worksheet.write(index, 9, customer)
            index+=1
        elif name in duplicate_name:
            if day_of_week == 2:
                worksheet.write(duplicate_name.index(name)+1, 3, '='+amount)
            elif day_of_week == 3:
                worksheet.write(duplicate_name.index(name)+1, 4, '='+amount)
            elif day_of_week == 4:
                worksheet.write(duplicate_name.index(name)+1, 5, '='+amount)
            elif day_of_week == 5:
                worksheet.write(duplicate_name.index(name)+1, 6, '='+amount)
            elif day_of_week == 6:
                worksheet.write(duplicate_name.index(name)+1, 7, '='+amount)
            elif day_of_week == 7:
                worksheet.write(duplicate_name.index(name)+1, 8, '='+amount)
            worksheet.write(index, 9, customer)

    worksheet.add_table('A1:J'+str(index+1), options)
    worksheet.set_column("A:A", 45)
    worksheet.set_column("C:I"+str(index+1), 10, number_format)

    workbook.close()
    file_on_memory.seek(0)

    return file_on_memory

def send_to_simple_xlsx_fix(data, file_name="Reporte Especiales2 Contado"+ str(datetime.today()).replace(":","")+".xlsx", sheet_name="Especiales_2", headers=None):

    file_on_memory = BytesIO()

    workbook = Workbook(file_on_memory)
    worksheet = workbook.add_worksheet(sheet_name)
    date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})
    number_format = workbook.add_format({'num_format': '#,##0.00'})
    wrap_format = workbook.add_format({'text_wrap': 0})
    bold = workbook.add_format({'bold': 1})
    row, col = 1, 0

    temp = []
    data_processed=[]
    duplicate_name=[]
    COLUMNAS = {'TOTAL':'C','LUNES':'D', 'MARTES':'E', 'MIÉRCOLES':'F', 'JUEVES': 'G', 'VIERNES' : 'H', 'SÁBADO': 'I'} 
    pos = 0
    index = 0

    for date,day_of_week,customer,name,amount,payment_method in data:
        name = (
            name.replace("TRAE","")
                .replace("CAJAS","")
                .replace("CAJA","")
                .replace("NO HIZO","")
                .replace("HIZO","")
                .replace("PEDIDOS","")
                .replace("PEDIDO","")
                .replace("SIN AZUCAR","")
                .replace("DOMOS","")
                .replace("DOMO","") 
                .replace("BANDEJAS","") 
                .replace("BANDEJA","")
                .replace("DMO MIXTO","")
                .replace("DMO MIXTA","")
                .replace("CASIT SURTI","")
                .replace(" CASIT ROSA","")
                .replace("  PARRILLA 2","")
                .replace(" CASIT 45 Y 20 AMARILLAS","")
            ).strip()

        if [name,date] not in temp:
            temp.append([name, date])
            data_processed.append([index,date,day_of_week,customer,name,str(amount),payment_method])
            index += 1
        elif [name,date] in temp:
            subindex = index-1
            data_processed[subindex][5] = '+'.join((str(data_processed[subindex][5]), str(amount)))


    index = 1
    for rowid, date,day_of_week,customer,name,amount,payment_method in data_processed:
        worksheet.write(index, 0, name)
        if name not in duplicate_name:
            duplicate_name.append(name)
            if day_of_week == 2:
                worksheet.write(index, 3, '='+amount, number_format)
            elif day_of_week == 3:
                worksheet.write(index, 4, '='+amount, number_format)
            elif day_of_week == 4:
                worksheet.write(index, 5, '='+amount, number_format)
            elif day_of_week == 5:
                worksheet.write(index, 6, '='+amount, number_format)
            elif day_of_week == 6:
                worksheet.write(index, 7, '='+amount, number_format)
            elif day_of_week == 7:
                worksheet.write(index, 8, '='+amount, number_format)
            #worksheet.write(index, 9, customer)
            index+=1
        elif name in duplicate_name:
            if day_of_week == 2:
                worksheet.write(duplicate_name.index(name)+1, 3, '='+amount, number_format)
            elif day_of_week == 3:
                worksheet.write(duplicate_name.index(name)+1, 4, '='+amount, number_format)
            elif day_of_week == 4:
                worksheet.write(duplicate_name.index(name)+1, 5, '='+amount, number_format)
            elif day_of_week == 5:
                worksheet.write(duplicate_name.index(name)+1, 6, '='+amount, number_format)
            elif day_of_week == 6:
                worksheet.write(duplicate_name.index(name)+1, 7, '='+amount, number_format)
            elif day_of_week == 7:
                worksheet.write(duplicate_name.index(name)+1, 8, '='+amount, number_format)
            #worksheet.write(index, 9, customer)
        worksheet.write_formula('C'+str(index), '=SUM('+COLUMNAS['LUNES']+str(index)+':'+COLUMNAS['SÁBADO']+str(index)+')')

    for DIA in COLUMNAS:
        worksheet.write_formula(COLUMNAS[DIA]+str(index+2), '=SUM('+COLUMNAS[DIA]+str(1)+':'+COLUMNAS[DIA]+str(index)+")")

    worksheet.set_column("A:A", 45)

    workbook.close()
    file_on_memory.seek(0)

    return file_on_memory


def send_to_xlsx(data, file_name="Reporte Especiales2 Contado " + str(datetime.today()).replace(":","")+".xlsx", sheet_name="Especiales_2", headers=None):

    workbook = Workbook(file_name)
    worksheet = workbook.add_worksheet(sheet_name)
    date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})
    number_format = workbook.add_format({'num_format': '#,##0.00'})
    bold = workbook.add_format({'bold': 1})

    row, col = 0, 0
    col_count = 0

    # headers = [header[0].replace("_", " ").upper() for header in data.description]
    

    [header.replace("_", " ").upper() for header in headers]
    worksheet.set_column(row,5,45)
    
    for header_name in headers:
        worksheet.write(row, col_count, header_name, bold)
        col_count += 1

    for line in data:
        row += 1
        for index in range(len(line)):
            print(line[index], isinstance(line[index], float))
            if isinstance(line[index], float):
                worksheet.write(row, index, float(line[index]), number_format)
            else:
                worksheet.write(row, index, line[index])

    workbook.close()

mysql = Odbc("MYSQL")
conn = mysql.connect(auto_commit=False)  # auto_comit defaul is false
cursor = conn.cursor()
result = cursor.execute(ESPECIALES_2_TO_EXCEL, '2022-06-20', '2022-06-25',0)
data = result.fetchall()


file = send_to_simple_xlsx_fix(data, headers=['fecha', 'COLUMNAS[DIA]', 'cliente', 'nombre', 'monto', 'forma'])

with open("excel_data2.xlsx", "w+b") as f:
    f.write(file.read())
    f.close()



 # repollo
 # cebolla
 # cilantro
 # aguates
 # ketchup
 # mayonesa
 # mostasa
 # tomate
 # chorizo extremeño
