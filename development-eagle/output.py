import mysql.connector as connector
from fpdf import FPDF
'''
Creates and saves a PDF to a directory within
the current OS deskptop directory.
'''
def output_data():
    
    try:
        cnx = connector.connect(user='test', password='test', host='localhost', database='EAGLEEYE')
    except:
        print("database connection unsuccessful")
        return
  
    
    data = "Select Query goes here"

    # PDF implementation goes here: 
        # try to store the PDF on your desktop after running
        
    '''
    pdf = FPDF()
    pdf.set_font("Arial", size=12)
    pdf.add_page()
    
    col_width = pdf.w / 4.5
    row_height = pdf.font_size
    for row in data:
        for item in row:
            pdf.cell(col_width, row_height*spacing,
                     txt=item, border=1)
        pdf.ln(row_height*spacing)
    
    HINT: Rename this to like [process_1.pdf or something]
    pdf.output('simple_table.pdf')
    '''

    
