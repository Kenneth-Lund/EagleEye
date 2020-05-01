import mysql.connector as connector
import datetime
import os
import pdfkit
import csv
  
# Creates default humand and machine readable output
def output(parameters, db_connection):
    
    cursor = db_connection.cursor()
    
    # Select data recently gathered from the time this process started
    data = cursor.execute("SELECT * FROM data_table WHERE time_retrieved > '%s'" % (str(parameters["time_started"]))) 
    rows = cursor.fetchall()
    
    # Create PDF
    default_pdf(rows, parameters)

    # Create CSV
    default_csv(rows, parameters)

    cursor.close()

    # Create Statistics report if specified by user
    if parameters["stat"]:

        try:
            statistics_pdf(parameters, db_connection)
        except Exception as e:
            print("Could not generate statistics PDF" + str(e))
            pass

    # Create a detailed history report if specified by user
    if parameters["detail"] != []:
        
        try:
            for data_type in parameters["detail"]:
            
                detail_pdf(parameters, db_connection, data_type)
        except Exception as e:
            print("Could not generate detail PDF" + str(e))
            pass

'''
Detailed report for specified data type
'''
def detail_pdf(parameters, db_connection, data_type):

    print("Creating detail PDF for detailing: " + data_type)

    style = '<style> table, th, td { border: 1px solid black; } </style>'

    title_html = '<html><head>' + style + '</head><body><h2>Eagle Eye</h2><p>Detailed ' + data_type + ' Report</p>'
    table_start_tag = '<table style="width:100%">'
    table_headers_row = '<tr> <th>Value</th> <th>Source</th> <th>Time Found</th> </tr>'
    table_end_tag='</table></body></html>'

    html = title_html + table_start_tag + table_headers_row

    cursor = db_connection.cursor()

    cursor.execute("SELECT data_table.data_value, data_table.data_source, data_table.time_retrieved FROM data_table WHERE data_type = '%s' ORDER BY time_retrieved" % (data_type)) 

    rows = cursor.fetchall()

    for row in rows:
        html_row = "<tr><td>" + str(row[0]) + "</td><td>" + str(row[1]) + "</td><td>" + str(row[2]) + "</td></tr>"

        html = html + html_row
        
    html = html + table_end_tag

    # END OF HTML GENERATION
    cursor.close()

    save_pdf(parameters, html, data_type)

'''
'''
def statistics_pdf(parameters, db_connection):
    
    print("Creating statistics PDF...")
    
    row_tag = '<tr>'
    end_row_tag = '</tr>'
    table_end_tag='</table>'

    style = '<style> table, th, td { border: 1px solid black; } </style>'

    # TABLE 1
    title_html = '<html><head>' + style + '</head><body><h2>Eagle Eye</h2><p>Statistics Report</p>'
    table_start_tag = '<table style="width:100%">'
    table_title = '<h2>Sensitive data type occurences:</h2>'
    table_headers_row = '<tr> <th>Phone</th> <th>Email</th> <th>SSN</th> <th>KEYWORD</th> </tr>'
    
    html = title_html + table_title + table_start_tag + table_headers_row + row_tag

    data_types = ['Phone', 'Email', 'SSN', 'KEYWORD']

    cursor = db_connection.cursor()

    for data_type in data_types:

        cursor.execute("SELECT COUNT(*) FROM data_table WHERE data_type = '%s'" % (data_type)) 
        rows = cursor.fetchall()

        if len(rows) > 0:

            html = html + '<td>' + str(rows[0][0]) + '</td>'
        
    html = html + end_row_tag + table_end_tag

    # TABLE 2
    table2_start_tag = '<table style="width:100%">'
    table2_title = '<h2>Sensitive data value occurences:</h2>'
    table2_headers_row = '<tr> <th>Data value</th> <th>Occurences</th></tr>'

    html = html + table2_start_tag + table2_title + table2_start_tag + table2_headers_row

    cursor.execute("Select data_table.data_value, COUNT(data_table.data_value) from data_table GROUP BY data_table.data_value ORDER BY COUNT(data_table.data_value)") 

    rows = cursor.fetchall()

    for row in rows:

        html = html + "<tr> <td>" + str(row[0]) + "</td> <td>" + str(row[1]) + "</td> </tr>"

    html = html + table_end_tag

    # TABLE 3
    table3_start_tag = '<table style="width:100%">'
    table3_title = '<h2>Sensitive data source occurences:</h2>'
    table3_headers_row = '<tr> <th>Source</th> <th>Occurences</th></tr>'

    html = html + table3_start_tag + table3_title + table3_start_tag + table3_headers_row

    cursor.execute("Select data_table.data_source, COUNT(data_table.data_source) from data_table GROUP BY data_table.data_source ORDER BY COUNT(data_table.data_source)") 

    rows = cursor.fetchall()

    for row in rows:

        html = html + "<tr> <td>" + str(row[0]) + "</td> <td>" + str(row[1]) + "</td> </tr>"

    html = html + table_end_tag

    # Table 4
    table4_start_tag = '<table style="width:100%">'
    table4_title = '<h2>Processes Analyzed:</h2>'
    table4_headers_row = '<tr> <th>Process</th> <th>Number of Data found</th></tr>'
    
    html = html + table4_start_tag + table4_title + table4_start_tag + table4_headers_row

    cursor.execute("Select processes.process_id, COUNT(processes.process_id) from processes GROUP BY processes.process_id ORDER BY COUNT(processes.process_id)") 

    rows = cursor.fetchall()

    for row in rows:

        html = html + "<tr> <td>" + str(row[0]) + "</td> <td>" + str(row[1]) + "</td> </tr>"

    html = html + table_end_tag + '</body></html>'
    
    # END OF HTML GENERATION
    cursor.close()

    save_pdf(parameters, html, "statistic")
    


'''
Creates default CSV
'''
def default_csv(rows, parameters):

    print("Creating CSV...")

    filename = "default+" + str(parameters["time_started"]) + ".csv"

    if parameters["filename"] is not None:
       filename = parameters["filename"] + "_default_" + str(parameters["time_started"]) + ".csv"

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

    style = '<style> table, th, td { border: 1px solid black; } </style>'

    # Create HTHML template string
    title_html = '<html><head>' + style + '</head><body><h2>Eagle Eye</h2><p>Detailed Report</p>'

    table_start_tag = '<table style="width:100%">'

    table_headers_row = '<tr> <th>Type</th> <th>Value</th> <th>Source</th> <th>Time Found</th> </tr>'

    table_end_tag='</table></body></html>'

    html = title_html + table_start_tag + table_headers_row

    for row in rows:
        html_row = "<tr><td>" + str(row[2]) + "</td><td>" + str(row[1]) + "</td><td>" + str(row[3]) + "</td><td>" + str(row[4]) + "</td></tr>"

        html = html + html_row
        
    html = html + table_end_tag

    save_pdf(parameters, html, "default")


def save_pdf(parameters, html, style):

    if parameters["filename"] is not None:
        pdfkit.from_string(html, os.path.join('./output', parameters["filename"] + '_' + style + '_' + str(parameters["time_started"]) + '.pdf'))
    else:
        pdfkit.from_string(html, os.path.join('./output', style + "_" + str(parameters["time_started"]) + ".pdf"))
    


'''
Creates and saves a PDF to a directory within
the current OS deskptop directory.
'''
def output_data(parameters, db_connection):

    output(parameters, db_connection)

    
    # Close database connection
    db_connection.commit()
    db_connection.close()  


