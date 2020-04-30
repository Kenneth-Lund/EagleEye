import mysql.connector as connector
import datetime
import os
import pdfkit
import csv
  
# Creates default humand and machine readable output
def default_output(parameters, db_connection):
    
    cursor = db_connection.cursor()

    data = cursor.execute("SELECT * FROM data_table") 
    rows = cursor.fetchall()
    
    # Create PDF
    default_pdf(rows, parameters)

    # Create CSV
    default_csv(rows, parameters)

    cursor.close()


'''
Creates default CSV
'''
def default_csv(rows, parameters):

    print("Creating CSV...")

    filename = "results_default.csv"

    if parameters["filename"] is not None:
       filename = parameters["filename"] + "_default.csv"

    with open(os.path.join('./output', filename), 'w') as csvfile:

        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Type', 'Value', 'Source', 'Time Found'])

        for row in rows:
            filewriter.writerow([str(row[2]), str(row[1]), str(row[3]), str(row[4])])

    print("Done")

'''
Creates default PDF
'''
def default_pdf(rows, parameters):

    print("Creating PDF...")

    # Create HTHML template string
    title_html = '<html><body><h2>Eagle Eye</h2><p>Process 1' + str(datetime.datetime.now()) + '</p>'

    table_start_tag = '<table style="width:100%">'

    table_headers_row = '<tr> <th>Type</th> <th>Value</th> <th>Source</th> <th>Time Found</th> </tr>'

    table_end_tag='</table></body></html>'

    html = title_html + table_start_tag + table_headers_row

    for row in rows:
        html_row = "<tr><td>" + str(row[2]) + "</td><td>" + str(row[1]) + "</td><td>" + str(row[3]) + "</td><td>" + str(row[4]) + "</td></tr>"

        html = html + html_row
        
    html = html + table_end_tag

    if parameters["filename"] is not None:
        pdfkit.from_string(html, os.path.join('./output', parameters["filename"] + '_default.pdf'))
    else:
        pdfkit.from_string(html, os.path.join('./output', "results_default.pdf"))


'''
Creates and saves a PDF to a directory within
the current OS deskptop directory.
'''
def output_data(parameters, db_connection):

    default_output(parameters, db_connection)

    
    # Close database connection
    db_connection.commit()
    db_connection.close()  


