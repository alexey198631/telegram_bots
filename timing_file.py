import gspread
import pandas as pd
import openpyxl
import config

filename = config.SERVICE_ACCOUNT
dairy_file = config.DAYS

gc = gspread.service_account(filename)
#wks = gc.open("my37").sheet1

# Open a sheet from a spreadsheet in one go
wks = gc.open("my37").worksheet('days')

# Get all the data from the sheet as a list of lists
data = wks.get_all_values()

# Convert the data to a pandas dataframe
df_new = pd.DataFrame(data[1:], columns=data[0])

# поиск индекса последнего элемента в колонке "column_name"
last_index = df_new.index[df_new['DEND'] == df_new['DEND'].max()].tolist()[-1]

df_new = df_new.loc[:last_index, :]



print(df_new.columns)


# Преобразование колонки в тип float
#df['float_col'] = df['float_col'].astype(float)

# Преобразование колонки в тип int
#df['int_col'] = df['int_col'].astype(int)

# Преобразование колонки в тип datetime
df_new['105'] = pd.to_datetime(df_new['105'], format='%d/%m/%Y')
df_new['DEND'] = pd.to_datetime(df_new['DEND'], format='%H:%M')
df_new['DEND'] = df_new['DEND'].dt.strftime('%H:%M')
df_new['DSTART'] = pd.to_datetime(df_new['DSTART'], format='%H:%M')
print(df_new.tail(5))
df_new.info()

# Load the workbook
workbook = openpyxl.load_workbook(dairy_file)

# Select the sheet you want to modify
sheet = workbook['copy']

# Извлекаем данные из листа и создаем DataFrame
data_days = sheet.values
cols = next(data_days)[0:]
df = pd.DataFrame(data_days, columns=cols)

print(df.tail(5))

df.info()





# Close the workbook
workbook.close()

diff_df = pd.merge(df, df_new, how='outer', indicator=True).query("_merge != 'both'").drop(columns='_merge')

writer = pd.ExcelWriter('data_files/experiment.xlsx', engine='xlsxwriter')
diff_df.to_excel(writer, sheet_name='cs')
writer.save()

"""

# Save the modified workbook
workbook.save()






writer = pd.ExcelWriter('timing_t.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='cs')
writer.save()


worksheet = wks.worksheet('Blad20')

# delete the sheet
wks.del_worksheet(worksheet)

"""






