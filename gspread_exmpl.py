import gspread

gc = gspread.service_account(filename='credentials.json')
sh = gc.open_by_key('1Q9bY3Vlc-He5eyyaZYllSE1h7XjRbduN2wR1zm4v31k')
worksheet = sh.sheet1

# res = worksheet.get_all_records()
# res = worksheet.get_all_values()
# res = worksheet.col_values(1)
# print(res)

new_book = ['Е.Замятин', 'роман-антиутопия', 'Мы', 'Д-503, О-90, I-330, Благодетель', 'Влияние тоталитаризма на жизнь человека, любовь, нравственный выбор', '']
worksheet.insert_row(new_book, 40)
