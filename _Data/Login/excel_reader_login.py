from openpyxl import load_workbook

FILE_PATH = r"_Data/Login/Login.xlsx"

def get_login_data(row_index=2):
    workbook    = load_workbook(FILE_PATH)
    sheet       = workbook["LOGIN"]

    # Menggunakan f-string untuk menggabungkan nama kolom dan nomor baris
    URL         = sheet[f"A{row_index}"].value
    USERNAME    = sheet[f"B{row_index}"].value
    PASSWORD    = sheet[f"C{row_index}"].value

    return {
        "URL": URL, 
        "USERNAME": USERNAME, 
        "PASSWORD": PASSWORD
        }