# Neopets Restock List Manager
This tool is intended to automate the process of extracting data from a user's Sale History and Neopet's item database and integrating it into Google Sheets.

One day, I will make this tool more user-friendly. :shipit:

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

## Limitations
This tool always adds to the first sheet within a spreadsheet (as indicated by "sheet1" in Line 36). I like to separate items based on the Neopian shop they stock in (each with their own sheet), so I unfortunately have to manually sort items before pasting them into "items.txt." If I can figure out how to link items to their corresponding shops, I will release another version that dynamically adds to sheets.

## Lastly...
Since this involves web scraping (an automated process), it may or may not be against Neopet's Terms of Service.

However, it should be noted that the intentions of this tool is **not** to cheat or give users an unfair advantage. It does not modify the website in any way, nor is it trying to farm for random events, Magma Pool times, etc. It just exports data to a Google spreadsheet. Additionally, I added a 5-second delay between each HTTP request as to not overload the server.
