import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

import re
import urllib.parse
import requests
import time
from bs4 import BeautifulSoup

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

    base_url = 'https://www.neopets.com/search.phtml?selected_type=object&string='

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
            # Scrape Neopets for estimated value
            encoded_item = urllib.parse.quote(new_item[1])
            url = base_url + encoded_item

            response = requests.get(url)

            est_value = 0
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                strong_values = soup.find_all('strong')

                rarity_string = strong_values[2].text.strip()
                value_string = strong_values[3].text.strip()
                rarity_int = int(rarity_string)
                # using re here since it takes a lot of time to parse through the HTML line
                value_int = int(re.search(r'\d+', value_string).group())

                # calculates restock price based on estimated value
                restock_price = round(value_int * 1.68)
                if rarity_int >= 95 and restock_price < 10000:
                    restock_price = 10000
                elif rarity_int >= 90 and restock_price < 5000:
                    restock_price = 5000
                elif rarity_int >= 85 and restock_price < 2500:
                    restock_price = 2500
            else:
                print(f'Failed to retrieve {new_item[1]}')

            # Add the new item if it doesn't exist in the sheet
            sheet.append_row([new_item[1], new_item[3], restock_price, '=D:D-E:E', new_item[0]], 
                value_input_option='USER_ENTERED', insert_data_option='INSERT_ROWS')
            
            print('Added: ' + new_item[1])

            time.sleep(5) # adding some delay for... safety

# Specify spreadsheet & file
file_path = 'items.txt'  # Replace with your file path
sheet_name = 'Restocking Reference'  # Replace with your Google Sheet name

data_from_file = read_text_file(file_path)
update_or_add_to_sheet(sheet_name, data_from_file)
