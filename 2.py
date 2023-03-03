import streamlit as st
import pandas as pd
import pdfplumber
from io import BytesIO

def pdf_to_excel(pdf_bytes):
    pdf_bytes=BytesIO(pdf_bytes.read())
    with pdfplumber.open(pdf_bytes) as pdf:
        ddf = []
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split('\n')
            try:
                header_index = lines.index("Sr No. AWB Number COID Client Name")
            except:
                header_index = lines.index("Sr No. AWB Number COID Client Name Remarks")
            columns = ["Sr No.", "AWB Number", "COID", "Client Name", "Remarks", "Extra"]
            rows = [line.split()[:5] + [' '.join(line.split()[5:])] for line in lines[header_index:]]
            newrows = []
            for row in rows:
                if len(row) == 5:
                    newrows.append(row .append(""))
                else:
                    newrows.append(row)
            df = pd.DataFrame(rows, columns=columns)
            df = df.drop(df[(~df['Sr No.'].str.isnumeric()) | (~df['COID'].str.startswith('(')) | (~df['COID'].str.endswith(')'))].index)
            ddf.append(df)
        result = pd.concat(ddf, ignore_index=True)
        result = result.reset_index(drop=True)
        result = result.rename(columns={
            'AWB Number': 'AWB Number1',
            'COID': 'AWB Number2',
            'Client Name': 'COID',
            'Remarks': 'Client Name',
            'Extra': 'Remarks'
        })
        result['AWB Number2'] = result['AWB Number2'].str.replace(r'\(|\)', '')
        result['COID'] = result['COID'].str[:-5]
        result = result.drop("Sr No." ,axis=1)
        return result

st.title("PDF to Excel Converter")

# File uploader widget
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Convert PDF to Excel
    df = pdf_to_excel(uploaded_file)

    # Download Excel file
    excel_bytes = BytesIO()
    df.to_excel(excel_bytes, index=False, header=True)
    excel_bytes.seek(0)
    st.download_button(
        label="Download Excel file",
        data=excel_bytes.getvalue(),
        file_name="result.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
