from sheets_connect import service
from settings import spreadsheet_id


# получение любой информации из таблицы по столбцам
def get_info(list_name, begin_letter, begin_digit, end_letter, end_digit):
    info = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='\'' + list_name + '\'!' + begin_letter + str(begin_digit) + ':' + end_letter + str(end_digit),
        majorDimension='COLUMNS'
    ).execute()
    return info["values"]


# вывод информации в таблицу по столбцам
def put_info(list_name, begin_letter, begin_digit, end_letter, end_digit, data):
    info = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": '\'' + list_name + '\'!' + begin_letter + str(begin_digit) + ':' + end_letter +
                          str(end_digit),
                 "majorDimension": "COLUMNS",
                 "values": data}]}).execute()
