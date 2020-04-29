import mysql.connector as connector
import datetime
import os
import pdfkit
'''
Creates and saves a PDF to a directory within
the current OS deskptop directory.
'''
def output_data(db_connection):

    # Create HTHML template string
    title_html = '<html><body><h2>Eagle Eye</h2><p>Process 1' + str(datetime.datetime.now()) + '</p>'

    table_start_tag = '<table style="width:100%">'

    table_headers_row = '<tr> <th>Type</th> <th>Value</th> <th>Source</th> <th>Time Found</th> </tr>'

    table_end_tag='</table></body></html>'

    html = title_html + table_start_tag + table_headers_row
    
    print("trying to query data")
    
    cursor = db_connection.cursor()

    data = cursor.execute("SELECT * FROM data_table") 
    rows = cursor.fetchall()
   
    for row in rows:
        html_row = "<tr><td>" + str(row[3]) + "</td><td>" + str(row[2]) + "</td><td>" + str(row[4]) + "</td><td>" + str(row[5]) + "</td></tr>"

        html = html + html_row
        
    html = html + table_end_tag

    print("Trying to make PDF")
    
    pdfkit.from_string(html, os.path.join('./output', "test.pdf"))

    print("DONE MAKING PDF")

    db_connection.commit()
    cursor.close()
    db_connection.close()    
    