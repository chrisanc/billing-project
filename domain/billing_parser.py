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
        
        
    def start(self):
        """
        Entry Point: Executes the file parsing and modifying.
        """
        # Parse the sheets
        generals, original_general = self.parse_generals()
        #totals, original_totals = self.parse("TOTALES")
        # Modify the Excel file
        self.modify_general(generals, original_general)
        #self.modify_totals(totals, original_totals)
    
    
    def parse_generals(self) -> tuple[list[pd.DataFrame], pd.DataFrame]:
        # Open the 'GENERALES' sheet
        df = self.file_manager.open_sheet("GENERALES")
        # Save up the original
        original = df
        # Get the headers from the dataset
        headers = df.dropna().iloc[0, :].apply(lambda x: x.upper().strip().replace(" ", "_")).to_list()
        # Get only the values with exactly 3 NaN values (bills)
        df = df[df.isna().sum(axis=1) == 3]
        # Set the headers
        df.columns = headers
        
        # Create a list to save the clean dataframes
        values: list[pd.DataFrame] = [pd.DataFrame(data=df.iloc[[0]], columns=headers)]
        # Iterate over the dataframe
        for i in range(1, len(df)):
            # If the latest added element has the same code
            if values[-1]["CODIGO_DEL_PAQUETE"].values[0] == df.iloc[i]["CODIGO_DEL_PAQUETE"]:
                values[-1] = pd.concat([values[-1], df.iloc[[i]]])
            else:
                values.append(pd.DataFrame(df.iloc[[i]], columns=headers))
                
        return values, original
    
    
    def parse(self, sheet_name: str) -> tuple[list[pd.DataFrame], pd.DataFrame]:
        """
        Parse the sheets to modify it.
        """
        # Read the dataframe
        df = self.file_manager.open_sheet(sheet_name)
        # Get the indices where the whole row doesn't contain a single NaN value.
        # Add the length of the dataframe at the end to modify all the elements
        indices = df.dropna().index.to_list() + [len(df)]
        # List to store the headers
        headers = list()
        # Variable to store the merged dataframe with the cleaned data
        values = list()
        
        # Algorithm to parse each billing card and merge in one.
        for i in range(len(indices) - 1):
            data = df.iloc[indices[i]:indices[i + 1], :]
            data = data[data.iloc[:, 1].notna()]
            # If the header list is still empty, we set it
            if len(headers) < 1:
                # Normalize and set the header
                headers = data.iloc[0].apply(lambda x : x.upper().strip().strip("*")).to_list()
                print(headers)
            data.columns = headers
            # Remove the first row (raw header)
            data = data[1:]
            
            # Append the clean data to the list
            values.append(data)
        
        return values, df
    
    
    def modify_general(self, dfs: list[pd.DataFrame], original: pd.DataFrame):
        """
        Usage of openpyxl to modify the original Excel file
        in-place using indices and absed on the clean dataframe
        """
        # Read the worksheet
        ws = self.file_manager.load_worksheet("GENERALES")
        # Iterate the dataframes
        for df in dfs:
            # Iterate the indices of the dataframe
            for idx in df.index:
                # Get the package code
                code = str(original.iloc[idx, 11]).strip()
                # Calculate the subtotal in MXN
                subt = round(self.dollar_price * self.prices[code], ndigits=4)
                # Set the code price
                ws.cell(row= idx + 2, column=14, value=self.prices[code])
                # Set the dollar price
                ws.cell(row=idx + 2, column=15, value=self.dollar_price)
                # Set the price in MXN
                ws.cell(row = idx + 2, column= 16, value=subt)
            # Manage the total row (final one)
            total_samples = len(df)
            # Set the subtotals
            ws.cell(row = df.index[-1] + 3, column = 14, value=round(total_samples * self.prices[code], ndigits=2))
            ws.cell(row= df.index[-1] + 3, column=17, value=round(total_samples * subt, ndigits=2))
        
        # Save the changes
        self.file_manager.workbook.save(self.file_manager.file)