import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Function to read data from the text file and parse it
def read_text_file(file_path):
    items = []
    with open(file_path, 'r') as file:
        for line in file:
            item_data = line.strip().split('\t') # list of a single item's properties (tab separated)

            date_obj = datetime.strptime(item_data[0], '%d/%m/%Y') # DD/MM/YYYY (string) -> DD/MM/YYYY (datetime)
            item_data[0] = date_obj.strftime('%m/%d/%y') # DD/MM/YYYY (datetime) -> MM/DD/YY (string)

            # not using re here bc this doesn't take a lot of time to parse + re gets complicated with "multiple numbers" in a string
            price = ''.join(filter(str.isdigit, item_data[3])) # Extracts number from price
            item_data[3] = int(price) # string -> int

            if item_data not in items:
                items.append(item_data)
    return items

# Function to update or add items to the Google Sheet
def update_or_add_to_sheet(sheet_name, items):
    # Use Google Sheets API credentials
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)

    # gspread - open sheet & get all values
    sheet = client.open(sheet_name).sheet1
    current_values = sheet.get_values()

    # Check each item in the input list
    for new_item in items:
        item_found = False

        for row_index, existing_item in enumerate(current_values): # Loops through all items in the list (including titles)
            if new_item[1] == existing_item[0]: # Finds item based on name
                item_found = True
                # Update the existing item in the sheet
                sheet.update_cell(row_index + 1, 2, new_item[3])  # Price in column B
                sheet.update_cell(row_index + 1, 5, new_item[0])  # Date in column E
                print('Updated: ' + new_item[1])
                break
        
        if not item_found:
            # Add the new item if it doesn't exist in the sheet
            sheet.append_row([new_item[1], new_item[3], '', '=B:B-C:C', new_item[0]], 
                value_input_option='USER_ENTERED', insert_data_option='INSERT_ROWS')
            
            print('Added: ' + new_item[1])

        current_values = sheet.get_values()

# Specify spreadsheet & file
file_path = 'items.txt'  # Replace with your file path
sheet_name = 'Restocking Reference'  # Replace with your Google Sheet name

data_from_file = read_text_file(file_path)
update_or_add_to_sheet(sheet_name, data_from_file)