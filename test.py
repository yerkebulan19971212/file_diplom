import pdfplumber
with pdfplumber.open(r'tessdft') as pdf:
    first_page = pdf.pages[0]
    print(len( pdf.pages))
    dsfg = first_page.extract_text()
    # print(first_page.extract_text())

print(dsfg[:100].replace(' ', ''))