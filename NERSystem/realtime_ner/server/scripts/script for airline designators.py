import xlrd
import re

#change to your own path
wb = xlrd.open_workbook(r"C:\Users\Andy\Desktop\data.xlsx")

sheet = wb.sheet_by_index(0)
#extract second column
sheet.cell_value(0, 0) 

file1 = open("grm.txt","a")#append mode
count200 = 1
for i in range(sheet.nrows):
    
    if i % 200 == 0:
        file1.write("\n\n")
        file1.write("AIRLINE_DESIGNATOR" + str(count200) + " = ")
        count200 = count200 + 1
    if (sheet.cell_value(i, 0)).count(' ') == 0:
        file1.write("(\"" + sheet.cell_value(i, 0).upper() + " \".utf8 <0.0005>) | ")
    if (sheet.cell_value(i, 0)).count(' ') == 1:
        file1.write("(\"" + sheet.cell_value(i, 0).upper().split(' ', 1)[0] + " \".utf8 " + "\"" +
              sheet.cell_value(i, 0).upper().split(' ', 2)[1] + " \".utf8 <0.0005>) | ")

    if (sheet.cell_value(i, 0)).count(' ') > 1:
        file1.write("(\"" + sheet.cell_value(i, 0).upper().split(' ', 1)[0] + " \".utf8 " + "\"" +
              sheet.cell_value(i, 0).upper().split(' ', 2)[1] + " \".utf8 " + "\"" +
              sheet.cell_value(i, 0).upper().split(' ', 3)[2] + " \".utf8 <0.0005>) | ")
    

        

#example ("AASCO".utf8 <0.005>)

file1.close()
