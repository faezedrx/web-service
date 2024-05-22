import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

# تنظیمات اعتبارنامه‌ها
credentials = service_account.Credentials.from_service_account_file(
    'credentials.json',
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)

# ID شیت و ID ورک شیت (GID)
SPREADSHEET_ID = '1GB0HaR13Ygb14qe_wTc4DBNs_QWxegfhbRVMv-4WNto'
WORKSHEET_ID = '1492129767'

# ایجاد سرویس
service = build('sheets', 'v4', credentials=credentials)

def get_sheet_data():
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=f'Sheet1!A:Z').execute()
    values = result.get('values', [])
    return values

def update_sheet_data(range, values):
    body = {
        'values': values
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range=range,
        valueInputOption='RAW', body=body).execute()
    return result

def append_row(values):
    body = {
        'values': [values]
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID, range=f'Sheet1!A:Z',
        valueInputOption='RAW', insertDataOption='INSERT_ROWS', body=body).execute()
    return result

def append_column(column_name, values):
    requests = [{
        'appendDimension': {
            'sheetId': WORKSHEET_ID,
            'dimension': 'COLUMNS',
            'length': 1
        }
    }]
    body = {
        'requests': requests
    }
    service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body).execute()

    last_col_index = len(df.columns) + 1
    range_ = f'Sheet1!{chr(64 + last_col_index)}1:{chr(64 + last_col_index)}{len(df) + 1}'
    values = [[column_name]] + [[value] for value in values]
    update_sheet_data(range_, values)

# دریافت داده‌ها
values = get_sheet_data()

# تبدیل داده‌ها به DataFrame
if not values:
    st.write('No data found.')
else:
    df = pd.DataFrame(values[1:], columns=values[0])
    st.write(df)

st.title("Google Sheets Data")

# فرم افزودن سطر جدید
st.subheader("Add a new row")
new_row = []
for column in df.columns:
    value = st.text_input(f'Enter {column}', key=f'new_{column}')
    new_row.append(value)

if st.button('Add Row'):
    append_row(new_row)
    st.success('Row added successfully!')

# فرم افزودن ستون جدید
st.subheader("Add a new column")
new_column_name = st.text_input('Enter new column name', key='new_column_name')
new_column_values = []
for i in range(len(df)):
    value = st.text_input(f'Enter value for row {i + 1}', key=f'new_col_value_{i}')
    new_column_values.append(value)

if st.button('Add Column'):
    append_column(new_column_name, new_column_values)
    st.success('Column added successfully!')
