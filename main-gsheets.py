import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# لینک به گوگل شیت شما
url = "https://docs.google.com/spreadsheets/d/1GB0HaR13Ygb14qe_wTc4DBNs_QWxegfhbRVMv-4WNto/edit?pli=1#gid=0"

# ایجاد اتصال به گوگل شیت
conn = st.connection("gsheets", type=GSheetsConnection)

# تابع برای خواندن داده‌ها از گوگل شیت
def read_data():
    return conn.read(spreadsheet=url, usecols=[0, 1])

# تابع برای افزودن داده به گوگل شیت
def add_data(new_data):
    df = read_data()
    updated_df = pd.concat([df, new_data], ignore_index=True)
    conn.write(updated_df, spreadsheet=url)

# تابع برای حذف داده از گوگل شیت
def delete_data(index):
    df = read_data()
    updated_df = df.drop(index).reset_index(drop=True)
    conn.write(updated_df, spreadsheet=url)

# تابع برای به‌روزرسانی داده در گوگل شیت
def update_data(index, updated_data):
    df = read_data()
    df.iloc[index] = updated_data
    conn.write(df, spreadsheet=url)

# نمایش داده‌ها
data = read_data()
st.dataframe(data)

# فرم برای افزودن داده جدید
with st.form(key='add_form'):
    new_col1 = st.text_input('Column 1')
    new_col2 = st.text_input('Column 2')
    submit_button = st.form_submit_button(label='Add Data')

if submit_button:
    new_data = pd.DataFrame([[new_col1, new_col2]], columns=data.columns)
    add_data(new_data)
    st.success('Data added successfully!')
    st.experimental_rerun()

# فرم برای به‌روزرسانی داده موجود
with st.form(key='update_form'):
    index_to_update = st.number_input('Index to update', min_value=0, max_value=len(data)-1, step=1)
    update_col1 = st.text_input('Updated Column 1', value=data.iloc[index_to_update, 0])
    update_col2 = st.text_input('Updated Column 2', value=data.iloc[index_to_update, 1])
    update_button = st.form_submit_button(label='Update Data')

if update_button:
    updated_data = [update_col1, update_col2]
    update_data(index_to_update, updated_data)
    st.success('Data updated successfully!')
    st.experimental_rerun()

# فرم برای حذف داده
with st.form(key='delete_form'):
    index_to_delete = st.number_input('Index to delete', min_value=0, max_value=len(data)-1, step=1)
    delete_button = st.form_submit_button(label='Delete Data')

if delete_button:
    delete_data(index_to_delete)
    st.success('Data deleted successfully!')
    st.experimental_rerun()
