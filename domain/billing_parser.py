from .file import File
import pandas as pd

class BillingParser:
    def __init__(self, dollar_price: float):
        self.dollar_price = dollar_price
        self.prices = {'010-CCW': 250, '008-CCS': 150, '009-CCP': 150, '001-FPI': 38, '002-FPC': 36, '003-FPP': 80, '004-WWS': 42, '005-INS': 21,
          '006-LSH': 50, '007-LSG': 26, '011-LIS': 35, '012-PCT': 75, '013-SPC': 35, '014-MIG': 10, '015-RPP': 80, '016-SAL': 35,
          '017-IRP': 35, '018-LIS': 75, '019-IRL': 35, '020-PWT': 30, '002-FPC': 36, '001-GAP': 13, '002-GAP': 14, '021-AGT': 25,
          'TFM-001': 80, 'TFM-003': 22, 'TFM-008': 32, 'TFM-009': 21, 'TFM-010': 38, 'TFM-011': 22, 'TFM-012': 495, 'TFM-013': 21,
          'TFM-014': 36, 'GIP-001': 3000 / self.dollar_price, 'CSS-001': 100, '003-GAP': 23, '021-LS6': 85, 'TFM-015': 160, 'TPA-015': 28}
        self.file_manager = File()
        
        
    def parse(self):
        generals = self.parse_generals()
        totals = self.parse_totals()
    
    
    def parse_generals(self) -> pd.DataFrame:
        """
        Parase
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
        
        return merged
    
    
    def modify_general(self, merged: pd.DataFrame):
        """
        Usage of openpyxl to modify the original Excel file
        in-place using indices and absed on the clean dataframe
        """
        pass
    
    
    def parse_totals(self) -> pd.DataFrame:
        df = self.file_manager.open_sheet("TOTALES")
        indices = df.dropna().index.to_list()