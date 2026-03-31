import pandas as pd

class TotalsParser:
    def __init__(self, prices: dict[str, float], dollar_price: float):
        self.__prices = prices
        self.__dollar_price = dollar_price
    
    
    def parse(self, df: pd.DataFrame, ws):
        totals, original = self.__parse_totals(df)
        self.__modify_totals(totals, ws)
    
    
    def __parse_totals(self, df: pd.DataFrame) -> tuple[list[pd.DataFrame], pd.DataFrame]:
        """
        Parse the sheets to modify it.
        """
        # Get the indexes without NaN
        idxs = df.dropna().index.to_list() + [len(df)]
        # Normalize column names
        headers = df.dropna().iloc[0, :].apply(lambda x : x.upper().strip().replace(" ", "_")).to_list()
        values = list()

        # Clean and save the dataframe card
        for i in range(1, len(idxs)):
            chunk = df.iloc[idxs[i - 1]:idxs[i], :].copy()
            chunk.columns = headers
            chunk = chunk.iloc[1:]
            values.append(chunk)
        
        return values, df
    
    
    def __modify_totals(self, dfs: list[pd.DataFrame], ws):
        # Iterate the dfs to manage each df
        for df in dfs:
            # Get the prices rows
            # First and last 3 ones are reserved, middle ones aren't.
            prices_mn = df[df["SAMPLE_FORM"].str.endswith("M.N.", na=False)].copy()
            
            # STEP 1: Set the dollar price
            ws.cell(row=prices_mn.index[0] + 2, column=3, value=f"$ {self.__dollar_price:.4f} MN")
            
            # STEP 2: Set the prices of each code
            subtotals = prices_mn[1:-3].copy()
            # Get the code price
            subtotals["CODE_PRICE"] = subtotals["CODIGO"].map(self.__prices)
            # Parse the total of samples
            subtotals["SAMPLES"] = subtotals["SAMPLE_FORM"].str.extract(r"(\d+)").astype(float)
            # Create a new column: SUBTOTAL
            subtotals["SUBTOTAL"] = subtotals["CODE_PRICE"] * subtotals["SAMPLES"] * self.__dollar_price
            # Modify the original file on each code info
            for row in subtotals.itertuples():
                ws.cell(row=row.Index + 2, column=3, value=f"{row.SAMPLES} X {round(row.CODE_PRICE * self.__dollar_price, ndigits=4):,} Pesos M.N.")
                ws.cell(row=row.Index + 2, column=4, value=row.SUBTOTAL)
            # Add the final subtotal (possible bug here, it's fragile)
            subtotal = round(subtotals["SUBTOTAL"].sum(), ndigits=4)
            ws.cell(row=subtotals.iloc[-1].name + 3, column=4, value=subtotal)
            
            # STEP 3: Set the subtotals in US and MXN, as well as the totals
            totals = prices_mn[-3:].copy()
            # Set the MXN and USD totals columns
            totals["MXN"] = [subtotal, round(subtotal * 0.16, ndigits=4), round(subtotal * 1.16, ndigits=4)]
            # USD convertions
            totals["USD"] = [
                round(subtotal / self.__dollar_price),
                round((subtotal / self.__dollar_price) * 0.16),
                round((subtotal / self.__dollar_price) * 1.16)
            ]
            # Set the values
            for row in totals.itertuples():
                ws.cell(row=row.Index + 2, column=3, value=f"{row.MXN:,} Pesos M.N.")
                ws.cell(row=row.Index + 2, column=4, value=f"{row.USD:,.2f} US Dollar")
            break