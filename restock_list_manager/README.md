# Neopets Restock List Manager
This tool is intended to automate the process of extracting data from a user's Sale History and Neopet's item database and integrating it into Google Sheets.

One day, I will make this tool more user-friendly. :shipit:


## Versions
1. `add_to_list.py` - includes web scraping; outputs item name, selling price, retail price, profit, & date
   
   <img src="https://github.com/astrobuns/neotools/assets/38766204/92958a26-c349-4969-9073-848d6c5de814" width="600">
   
2. `add_to_list2.py` - no web scraping; outputs item name, selling price, profit, & date
   
   <img src="https://github.com/astrobuns/neotools/assets/38766204/fcdb7b66-375b-4689-9942-8040c09aa3ed" width="600">

3. `add_to_list3.py` - no web scraping; outputs item name, selling price, & date
   
   <img src="https://github.com/astrobuns/neotools/assets/38766204/ab2699c4-99d0-4cf6-af0b-6be6af5bd914" width="370">

4. `add_to_list4.py` - #1 but with added support for adding items from different shops to different sheets within the spreadsheet, assuming that the sheet name is the shop's name **as it appears on Neopets** (except for "Refreshments" and "Ugga Shinies", since they're both labeled "Shops" in-game for some reason)

Note: Tools without web scraping will run faster mostly because they do not have an added delay.


## Assumptions Before Starting
1. The first part of this tool will extract data from a text file containing the user's Sale History. By default, directly copying and pasting your Sale History **(not including the headers)** into a text file will result in:

   - each item on a new line
   - each item property on the same line, tab-separated

   The following is an example of this:
   ```
   21/12/2023	Fire Toast	anthony_co	1,600 NP
   21/12/2023	Hot Dog and Beans Pie	zirma	1,200 NP
   ```

2. This tool assumes that a "logical table of data" is able to be found within the sheet. Make sure you have your data formatted as a table or any "rows" that this tool tries to add will turn out wonky. If you have multiple tables in a single sheet, then you will have to specify a table range within the sheet.append_row() function in Lines 84-85. Assuming *x* is the range in A1 notation:
   
   ```python
   sheet.append_row([new_item[1], new_item[3], restock_price, '=B:B-C:C', new_item[0]],
      value_input_option='USER_ENTERED', insert_data_option='INSERT_ROWS', table_range='x')
   ```

   However, I wouldn't recommend having multiple tables in a single sheet anyways, since Google Sheet's filters can't really be applied to all of them.


## How to Run the Program
On top of the program itself, you will also need two additional files in the same directory:

1. credentials.json
   - For getting the file: https://support.google.com/cloud/answer/6158849?hl=en
   - For enabling the Google Drive and Google Sheets API: https://support.google.com/googleapi/answer/6158841?hl=en
2. items.txt
   - Copy and paste your Sale History as previously described.

To run the program, run `python [insert file name here].py` in the directory where all three of these files are located.


## Lastly...
Tools that involve web scraping (an automated process) may or may not be against Neopet's Terms of Service.

However, it should be noted that the intentions of this tool is **not** to cheat or give users an unfair advantage. It does not modify the website in any way, nor is it trying to farm for random events, Magma Pool times, etc. It just exports data to a Google spreadsheet. Additionally, I added a 5-second delay between each HTTP request as to not overload the server. (Without the delay, you will run into a connection error about 30 items in.)

If in the future, TNT states outright that any form of automation is not allowed, I will be getting rid of the tools with web scraping.
