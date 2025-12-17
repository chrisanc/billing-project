# **💰 Billing filler project**
**Stack:** Python

## **What´s this project about?**
This project was developed with the purpose of making the job of people easier by using this to fill their billings.

User must provide the program 2 things to make it work the right way:
- **Excel file with the empty billing:** This Excel file has a known format. We modify the file by mapping the empty cells that should contain data.
- **Exchange rate between MXN and USD in the desired date:** The USD price agaisn´t the MXN in some date.

This two things are the heart of the system and they should be in the right format if you want to have the results you need.

When you run the program and you provide it the two arguments, it will modify the Excel file in place with the whole data in it, making the process faster than filling it manually.

## ✍️ Manual filling vs this project:
If you filled a billing manually, it would take you about 40-50 minutes to finish and you could make mistakes with the calculations but, if you use this system, it takes you about 2-3 minutes
and it won´t make any mistake because the data is managed in a very precise way.

## 📖 Libraries needed
To be able to run this project, you must install the next dependencies:

```cmd
pip install openpyxl
pip install pandas
pip install tkinter
```

**openpyxl:** Library used to load the excel and modify the cells in it.

**pandas:** Library used to create dataframes and make stadistic calculus.

**tkinter:** Library to display a file dialog and make the user navigate through their file system so they can choose their Excel file.
