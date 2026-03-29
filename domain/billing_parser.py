from .file import File
import pandas as pd

class BillingParser:
    def __init__(self, dollar_price: float):
        # Current dollar price
        self.dollar_price = dollar_price
        # Code-Price relation (USD)
        self.prices = {'010-CCW': 250, '008-CCS': 150, '009-CCP': 150, '001-FPI': 38, '002-FPC': 36, '003-FPP': 80, '004-WWS': 42, '005-INS': 21,
          '006-LSH': 50, '007-LSG': 26, '011-LIS': 35, '012-PCT': 75, '013-SPC': 35, '014-MIG': 10, '015-RPP': 80, '016-SAL': 35,
          '017-IRP': 35, '018-LIS': 75, '019-IRL': 35, '020-PWT': 30, '002-FPC': 36, '001-GAP': 13, '002-GAP': 14, '021-AGT': 25,
          'TFM-001': 80, 'TFM-003': 22, 'TFM-008': 32, 'TFM-009': 21, 'TFM-010': 38, 'TFM-011': 22, 'TFM-012': 495, 'TFM-013': 21,
          'TFM-014': 36, 'GIP-001': 3000 / self.dollar_price, 'CSS-001': 100, '003-GAP': 23, '021-LS6': 85, 'TFM-015': 160, 'TPA-015': 28}
        # Instanciate the file manager
        self.file_manager = File()
        
        
    def parse(self):
        """
        Entry Point: Executes the file parsing and modifying.
        """
        # Parse the sheets
        generals_merged, generals = self.parse_generals()
        totals = self.parse_totals()
        # Modify the Excel file
        self.modify_general(generals_merged, generals)
    
    
    def parse_generals(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Parse the 'GENERALES' sheet to modify it.
        """
        # Read the dataframe
        df = self.file_manager.open_sheet("GENERALES")
        # Get the indices where the whole row doesn't contain a single NaN value
        indices = df.dropna().index.to_list()
        # List to store the headers
        headers = list()
        # Variable to store the merged dataframe with the cleaned data
        merged = None
        
        # Algorithm to parse each billing card and merge in one.
        for i in range(len(indices) - 1):
            data = df.iloc[indices[i]:indices[i + 1], :]
            data = data[data.iloc[:, 1].notna()]
            # If the header list is still empty, we set it
            if len(headers) < 1:
                # Normalize and set the header
                headers = data.iloc[0].apply(lambda x : x.upper().strip().strip("*"))
            data.columns = headers
            # Remove the first row (raw header)
            data = data[1:]
            
            # If the merged dataset isn't set, we set it
            if merged is None:
                merged = data
                continue
            # Concat the dataframes
            merged = pd.concat([merged, data])
        
        return merged, df
    
    
    def modify_general(self, merged: pd.DataFrame, original: pd.DataFrame):
        """
        Usage of openpyxl to modify the original Excel file
        in-place using indices and absed on the clean dataframe
        """
        # Read the worksheet
        ws = self.file_manager.load_worksheet("GENERALES")
        # Iterate the indices
        for idx in merged.index:
            # Get the package code
            code = str(original.iloc[idx, 11]).strip()
            # Set the dollar price
            ws.cell(row=idx + 2, column=14, value=self.dollar_price)
            # Set the code price
            ws.cell(row= idx + 2, column=15, value=self.prices[code])
            # Set the price in MXN
            ws.cell(row = idx + 2, column= 16, value=f"{self.dollar_price * self.prices[code]:,.2f}")
        
        # Save the changes
        self.file_manager.workbook.save(self.file_manager.file)
    
    
    def parse_totals(self) -> pd.DataFrame:
        """
        Parse the 'TOTALES' sheet to modify it.
        """
        df = self.file_manager.open_sheet("TOTALES")
        indices = df.dropna().index.to_list()
        
        return df