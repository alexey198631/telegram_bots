import gspread
import pandas as pd
import config

filename = config.SERVICE_ACCOUNT

gc = gspread.service_account(filename)
wks = gc.open("my37").sheet1

print(wks)

"""
# Open a sheet from a spreadsheet in one go
wks = gc.open("my37").worksheet('timing')


# Get all the data from the sheet as a list of lists
data = wks.get_all_values()

# Convert the data to a pandas dataframe
df = pd.DataFrame(data[1:], columns=data[0])


writer = pd.ExcelWriter('timing_t.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='cs')
writer.save()


worksheet = wks.worksheet('Blad20')

# delete the sheet
wks.del_worksheet(worksheet)

"""




