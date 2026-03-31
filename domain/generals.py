import pandas as pd

class GeneralParser:
    def __init__(self, prices: dict[str, float], dollar_price: float):
        self.__prices = prices
        self.__dollar_price = dollar_price
        
        
    def parse(self, df: pd.DataFrame, ws):
        # Parse the sheet
        generals, original = self.__parse_generals(df)
        # Modify the file
        self.__modify_general(generals, original, ws)
    
    
    def __parse_generals(self, df: pd.DataFrame) -> tuple[list[pd.DataFrame], pd.DataFrame]:
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
    
    
    def __modify_general(self, dfs: list[pd.DataFrame], original: pd.DataFrame, ws):
        """
        Usage of openpyxl to modify the original Excel file
        in-place using indices and absed on the clean dataframe
        """
        # Iterate the dataframes
        for df in dfs:
            # Iterate the indices of the dataframe
            for idx in df.index:
                # Get the package code
                code = str(original.iloc[idx, 11]).strip()
                # Calculate the subtotal in MXN
                subt = round(self.__dollar_price * self.__prices[code], ndigits=4)
                # Set the code price
                ws.cell(row= idx + 2, column=14, value=self.__prices[code])
                # Set the dollar price
                ws.cell(row=idx + 2, column=15, value=self.__dollar_price)
                # Set the price in MXN
                ws.cell(row = idx + 2, column= 16, value=subt)
            # Manage the total row (final one)
            total_samples = len(df)
            # Set the subtotals
            ws.cell(row = df.index[-1] + 3, column = 14, value=round(total_samples * self.__prices[code], ndigits=2))
            ws.cell(row= df.index[-1] + 3, column=17, value=round(total_samples * subt, ndigits=2))