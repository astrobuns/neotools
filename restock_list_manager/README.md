# Neopets Restock List Manager
This tool is intended to automate the process of extracting data from a user's Sale History and Neopet's item database and integrating it into Google Sheets.

## Assumptions Before Starting
1. The first part of this tool will extract data from a text file containing the user's Sale History. By default, directly copying and pasting your Sale History **(not including the headers)** into a text file will result in:

   - each item on a new line
   - each item property on the same line, tab-separated

   The following is an example of this:
   ```
   21/12/2023	Fire Toast	anthony_co	1,600 NP
   21/12/2023	Hot Dog and Beans Pie	zirma	1,200 NP
   ```

3. The `gspread` library is generally able to detect a "logical table of data" within the sheet. If this is not the case—for example, if you have multiple tables in a single sheet—then you may specify a table range within the sheet.append_row() function. Specifically, the parameter is `table_range='x'`, where x is whatever the range is in A1 notation. However, I wouldn't recommend having multiple tables in a single sheet anyways, since Google Sheet's filters can't really be applied to all of them.

5. This tool formats the spreadsheet in a specific way. The order in which it outputs data, from first to last, is: item name, selling price, restock price, profit, and date.

## How to Run the Program
 
