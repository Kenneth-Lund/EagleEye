import mysql.connector as connector
from fpdf import FPDF
import os
'''
Creates and saves a PDF to a directory within
the current OS deskptop directory.
'''
def output_data(db_connection):

    with open(os.path.join('./output', "test.txt"), "w") as f:
        f.write("this is a test")

    f.close()
    # How to clsoe db_connection: db_connection.close()

    print("trying to query data")
    
    cursor = db_connection.cursor()

    data = cursor.execute("SELECT * FROM data_table") 
    rows = cursor.fetchall()

    # create PDF from queried data

    print("trying to make a pdf now")

    pdf = FPDF()
    pdf.set_font("Arial", size=8)
    pdf.add_page()

    print(str(len(rows)))

    spacing = 1    
    col_width = pdf.w / 7
    row_height = pdf.font_size
    for row in rows:
        for item in row:
            pdf.cell(col_width, row_height*spacing, txt=str(item), border=1)
        pdf.ln(row_height*spacing)

    pdf.output(dest='S').encode('latin-1')

    print("DONE MAKING PDF")

    db_connection.commit()
    cursor.close()
    db_connection.close()    
