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

            if item_data not in items:
                items.append(item_data)
    return items

# Function to update or add items to the Google Sheet
def update_or_add_to_sheet(sheet_name, items):
    shop_dict = {
        "1": "Neopian Fresh Foods",
        "2": "Kauvara's Magic Shop",
        "3": "Toy Shop",
        "4": "Unis Clothing Shop",
        "5": "Grooming Parlour",
        "7": "Magical Bookshop",
        "8": "Collectable Card Shop",
        "9": "Battle Magic",
        "10": "Defence Magic",
        "12": "Neopian Garden Centre",
        "13": "Neopian Pharmacy",
        "14": "Chocolate Factory",
        "15": "The Bakery",
        "16": "Neopian Health Foods",
        "17": "Neopian Gift Shop",
        "18": "Smoothie Store",
        "20": "Tropical Food Shop",
        "21": "Tiki Tack",
        "22": "Grundos Cafe",
        "23": "Space Weaponry",
        "24": "Space Armour",
        "25": "The Neopian Petpet Shop",
        "26": "The Robo-Petpet Shop",
        "27": "The Rock Pool",
        "30": "Spooky Food",
        "31": "Spooky Petpets",
        "34": "The Coffee Cave",
        "35": "Slushie Shop",
        "36": "Ice Crystal Shop",
        "37": "Super Happy Icy Fun Snow Shop",
        "38": "Faerieland Bookshop",
        "39": "Faerie Foods",
        "40": "Faerieland Petpets",
        "41": "Neopian Furniture",
        "42": "Tyrannian Foods",
        "43": "Tyrannian Furniture",
        "44": "Tyrannian Petpets",
        "45": "Tyrannian Weaponry",
        "46": "Hubert's Hot Dogs",
        "47": "Pizzaroo",
        "48": "Usukiland",
        "49": "Lost Desert Foods",
        "50": "Peopatra's Petpets",
        "51": "Sutek's Scrolls",
        "53": "Neopian School Supplies",
        "54": "Sakhmet Battle Supplies",
        "55": "Osiri's Pottery",
        "56": "Merifoods",
        "57": "Ye Olde Petpets",
        "58": "Neopian Post Office",
        "59": "Haunted Weaponry",
        "60": "Spooky Furniture",
        "61": "Wintery Petpets",
        "62": "Jelly Foods",
        "63": "Refreshments", # Shops
        "66": "Kiko Lake Treats",
        "67": "Kiko Lake Carpentry",
        "68": "Collectable Coins",
        "69": "Petpet Supplies",
        "70": "Booktastic Books",
        "71": "Kreludan Homes",
        "72": "Cafe Kreludor",
        "73": "Kayla's Potion Shop",
        "74": "Darigan Toys",
        "75": "Faerie Furniture",
        "76": "Roo Island Souvenirs",
        "77": "Brightvale Books",
        "78": "The Scrollery",
        "79": "Brightvale Glaziers",
        "80": "Brightvale Armoury",
        "81": "Brightvale Fruits",
        "82": "Brightvale Motery",
        "83": "Royal Potionery",
        "84": "Neopian Music Shop",
        "85": "Lost Desert Medicine",
        "86": "Collectable Sea Shells",
        "87": "Maractite Marvels",
        "88": "Maraquan Petpets",
        "89": "Geraptiku Petpets",
        "90": "Qasalan Delights",
        "91": "Desert Arms",
        "92": "Words of Antiquity",
        "93": "Faerie Weapon Shop",
        "94": "Illustrious Armoury",
        "95": "Exquisite Ambrosia",
        "96": "Magical Marvels",
        "97": "Legendary Petpets",
        "98": "Plushie Palace",
        "100": "Wonderous Weaponry",
        "101": "Exotic Foods",
        "102": "Remarkable Restoratives",
        "103": "Fanciful Fauna",
        "104": "Chesterdrawers' Antiques",
        "105": "The Crumpetmonger",
        "106": "Neovian Printing Press",
        "107": "Prigpants & Swolthy, Tailors",
        "108": "Mystical Surroundings",
        "110": "Lampwyck's Lights Fantastic",
        "111": "Cog's Togs",
        "112": "Molten Morsels",
        "113": "Moltaran Petpets",
        "114": "Moltaran Books",
        "116": "Springy Things",
        "117": "Ugga Shinies" # Shops
    }

    # Use Google Sheets API credentials
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)

    base_url = 'https://www.neopets.com/search.phtml?selected_type=object&string='

    # Check each item in the input list
    for new_item in items:
        # scraping setup
        encoded_item = urllib.parse.quote(new_item[1])
        url = base_url + encoded_item
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # scrape for shop & open corresponding sheet
        shop = soup.find('input', {'name' :'obj_type'}).get('value')
        sheet = None
        try:
            sheet = client.open(sheet_name).worksheet(shop_dict[shop])
        except: # WorksheetNotFound
            spreadsheet = client.open(sheet_name)
            spreadsheet.add_worksheet(shop_dict[shop], 1000, 26) # add sheet with that shop name, default number of rows & columns
            sheet = client.open(sheet_name).worksheet(shop_dict[shop])
        current_values = sheet.get_values()
        
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
            if response.status_code == 200:
                # scrape for est value & rarity
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
            sheet.append_row([new_item[1], new_item[3], restock_price, '=B:B-C:C', new_item[0]], 
                value_input_option='USER_ENTERED', insert_data_option='INSERT_ROWS')
            
            print('Added: ' + new_item[1])

        current_values = sheet.get_values()

        time.sleep(5) # adding some delay for... safety

# Specify spreadsheet & file
file_path = 'items.txt'  # Replace with your file path
sheet_name = 'Restocking Reference'  # Replace with your Google Sheet name

data_from_file = read_text_file(file_path)
update_or_add_to_sheet(sheet_name, data_from_file)
