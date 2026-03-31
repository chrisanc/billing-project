from .file import File
from .generals import GeneralParser
from .totals import TotalsParser
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
        self.generals = GeneralParser(self.prices, self.dollar_price)
        self.totals = TotalsParser(self.prices, self.dollar_price)
        
        
    def start(self):
        """
        Entry Point: Executes the file parsing and modifying.
        """
        # Parse and modify the generals sheet
        #self.generals.parse(self.file_manager.open_sheet("GENERALES"), self.file_manager.load_worksheet("GENERALES"))
        # Parse and modify the totals sheet
        self.totals.parse(self.file_manager.open_sheet("TOTALES"), self.file_manager.load_worksheet("TOTALES"))
        # Save the changes to the original file
        self.file_manager.workbook.save(self.file_manager.file)