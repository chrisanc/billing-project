from tkinter import filedialog
from openpyxl import load_workbook
import pandas as pd

"""
File class: Used to manage the files in the system
"""
class File:
    def __init__(self):
        self.file = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        
    def open_sheet(self, sheet_name: str):
        return pd.read_excel(self.file, sheet_name = sheet_name)
        
    def load_workbook(self):
        return load_workbook(self.file)