import gspread_asyncio
from google.oauth2.service_account import Credentials
import config_io
import datetime

link = config_io.get_value('SHEET_LINK')

WORKSHEET_BUFFER = 0
WORKSHEET_CONFIG = 1
WORKSHEET_WORK_NOTES = 2

def get_creds():
    creds = Credentials.from_service_account_file("key.json")
    scoped = creds.with_scopes([
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ])
    return scoped


agcm = gspread_asyncio.AsyncioGspreadClientManager(get_creds)

async def get_sheet(agcm=agcm, worksheet_number=0):
    agc = await agcm.authorize()
    ss = await agc.open_by_url(link)
    zero_ws = await ss.get_worksheet(worksheet_number)
    return zero_ws


async def get_all_values(worksheet_number):
    sheet = await get_sheet(worksheet_number=worksheet_number)
    all_values = await sheet.get_all_values()
    return all_values

async def get_user(id_tg):
    result = None
    all_ids_numbers = await get_all_values(WORKSHEET_BUFFER)
    for row in all_ids_numbers:
        if str(row[0]).isdecimal() and int(row[0]) == int(id_tg):
            result = row
    return result

async def get_number_recommendation(id_tg):
    result = None
    all_ids_numbers = await get_all_values(WORKSHEET_BUFFER)
    for row in all_ids_numbers:
        if str(row[0]).isdecimal() and int(row[0]) == int(id_tg):
            result = str(row[2])
    return result

async def get_city_recommendation():
    all_config_data = await get_all_values(WORKSHEET_CONFIG)
    result = []
    for row in all_config_data[1:]:
        if len(row) > 0 and row[0].strip():
            result.append(row[0].strip())
    if len(result):
        return result
    return None

async def get_type_work_recommendation():
    all_config_data = await get_all_values(WORKSHEET_CONFIG)
    result = []
    for row in all_config_data[1:]:
        if len(row) > 0 and row[1].strip():
            result.append(row[1].strip())
    if len(result):
        return result
    return None

async def get_narrative_recommendation():
    all_config_data = await get_all_values(WORKSHEET_CONFIG)
    result = []
    for row in all_config_data[1:]:
        if len(row) > 0 and row[2].strip():
            result.append(row[2].strip())
    if len(result):
        return result
    return None

async def get_type_transport_recommendation():
    all_config_data = await get_all_values(WORKSHEET_CONFIG)
    result = []
    for row in all_config_data[1:]:
        if len(row) > 0 and row[3].strip():
            result.append(row[3].strip())
    if len(result):
        return result
    return None


async def append_row_to_work_notes(row_data):
    sheet = await get_sheet(worksheet_number=WORKSHEET_WORK_NOTES)
    await sheet.append_row(row_data)

async def append_row_to_buffer(row_data):
    sheet = await get_sheet(worksheet_number=WORKSHEET_BUFFER)
    await sheet.append_row(row_data)


async def update_cell_buffer(id_tg, column_to_update, value):
    """row начинается с 1, не как в массивах"""

    sheet = await get_sheet(worksheet_number=WORKSHEET_BUFFER)
    all_values = await sheet.get_all_values()

    for row_index, row in enumerate(all_values, start=1):
        if len(row) > 0 and str(row[0]).isdecimal() and int(row[0]) == int(id_tg):
            await sheet.update_cell(row_index, column_to_update, value)
            return True

    return False
    
    
    

