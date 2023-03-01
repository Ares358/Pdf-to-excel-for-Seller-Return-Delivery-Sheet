import streamlit as st
import pandas as pd
import re 
from io import BytesIO
import base64
from PyPDF2 import PdfFileReader

def extract_data(file):

    def extract_date(file):
        datetime_regex = r"\b(\d{1,2}\s+\w+,\s+\d{4})\b"
        with pdfplumber.open(file) as pdf:
            # Loop through all the pages in the PDF
            for page in pdf.pages:
                # Extract text from the page
                text = page.extract_text()
                # Extract datetime from the page and write to the Excel sheet
                datetime = re.search(datetime_regex, text)
                if datetime:
                    finalDate = datetime.group()
        return finalDate

    # Call the extract_data function to extract the date from the PDF
    finalDate = extract_date(pdf_path)

    # Get the total number of pages in the PDF
    total_pages = len(cam.read_pdf(pdf_path, pages="all"))

    # Initialize an empty list to store the tables
    all_tables = []

    # Loop through each page and extract the tables
    for page in range(1, total_pages+1):
        tables = cam.read_pdf(pdf_path, pages=str(page))
        all_tables.extend(tables)

    # Concatenate all the tables into one dataframe
    # df = pd.concat([table.df for table in all_tables])
    df = pd.concat([table.df.iloc[1:] for table in all_tables])

    # Select the columns you want to keep and rename them
    df = df.drop([0,3], axis=1) # Remove columns 0 and 3
    print(df)
    df = df.rename(columns={1: "AWB Number", 2: "COID", 4: "Remarks"}) # Rename columns 1, 2, and 4
    df['AWB Number2'] = df['AWB Number'].str.extract(r'\((.*)\)')
    df['Order ID1'] = df['COID'].str.extract(r'(.*)_\d+_\w+$')
    df = df[['AWB Number', 'AWB Number2', 'Order ID1', 'Remarks']]
    df = df.rename(columns={'AWB Number': 'AWB Number1', 'Order ID1': 'Order ID'})
    df['AWB Number'] = df['AWB Number1'].str.extract(r'^(\S+)')
    df['Date'] = finalDate
    df = df[['AWB Number', 'AWB Number2', 'Order ID', 'Remarks', 'Date']]

    # df.insert(1, "AWB Number2", "") # Add new "AWB Number2" column
    df['Date'] = finalDate # Add finalDate to new "Date" column
    return df

st.title("PDF Data Extraction")

# File uploader
file = st.file_uploader("Upload a PDF file", type="pdf")

if file is not None:
    # Extract data and display in a table
    file.seek(0)
    df = extract_data(file)
    st.write(df)

    # Download button for Excel file
    output = BytesIO()
    excel_file = df.to_excel(output, index=False)
    b64 = base64.b64encode(output.getvalue()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="pdf_convert.xlsx">Download Excel file</a>'
    st.markdown(href, unsafe_allow_html=True)
else:
    st.write("Please upload a PDF file.")


# import streamlit as st
# import tabula as tb
# import pandas as pd
# import pdfplumber
# import re 
# from io import BytesIO
# import base64

# def extract_data(file):
#     datetime_regex = r"\b(\d{1,2}\s+\w+,\s+\d{4})\b"
# #     file2 = BytesIO(file.read())
#     with pdfplumber.open(file) as pdf:
#         # Loop through all the pages in the PDF
#         for page in pdf.pages:
#             # Extract text from the page
#             text = page.extract_text()
#             # Extract datetime from the page and write to the Excel sheet
#             datetime = re.search(datetime_regex, text)
#             if datetime:
#                 finalDate = datetime.group()
#     print("In1",finalDate, flush=True)
    
#     # csv file
#     file.seek(0)
#     table = tb.read_pdf(file, pages='all')
    
#     #csv_table = tb.convert_into(file, 'pdf_convert.csv', output_format='csv', pages='all')

#     # for excel extraction, we have to export the data to the dataframe
#     # Select only the columns you need

#     # we are using pandas library
#     df = pd.concat(table)
#     # extract the part in parentheses as a separate column
#     df['AWB Number2'] = df['AWB Number'].str.extract(r'\((.*)\)')
#     df['Order ID1'] = df['COID'].str.extract(r'(.*)_\d+_\w+$')
#     df = df[['AWB Number', 'AWB Number2', 'Order ID1', 'Remarks']]
#     df = df.rename(columns={'AWB Number': 'AWB Number1', 'Order ID1': 'Order ID'})
#     df['AWB Number'] = df['AWB Number1'].str.extract(r'^(\S+)')
#     df['Date'] = finalDate
#     df = df[['AWB Number', 'AWB Number2', 'Order ID', 'Remarks', 'Date']]
#     return df

# st.title("PDF Data Extraction")

# # File uploader
# file = st.file_uploader("Upload a PDF file", type="pdf")
# # file = BytesIO(file.read())

# if file is not None:
#     # Extract data and display in a table
#     file.seek(0)
#     df = extract_data(file)
#     st.write(df)

#     # Download button for Excel file
#     output = BytesIO()
#     excel_file = df.to_excel(output, index=False)
#     b64 = base64.b64encode(output.getvalue()).decode()
#     href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="pdf_convert.xlsx">Download Excel file</a>'
#     st.markdown(href, unsafe_allow_html=True)
# else:
#     st.write("Please upload a PDF file.")
