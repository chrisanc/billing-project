# UI
import streamlit as st
# Date management libraries
from datetime import datetime as dt, timedelta as td
# RegEx
import re
# Banxico
from banxico_sie import BanxicoSIEClient, Currency
from .helper import months, shift_weekend
from domain.billing_parser import BillingParser
# .env files
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# UI Functionality using Streamlit.
# The goal is to create a useful, pretty and intuitive UI for users.

def run_ui():
    # Display basic information about the system
    st.title("Automation")
    st.text("Created by: Christian Sánchez.")

    # Banxico Client initialization
    client = BanxicoSIEClient(os.getenv("BANXICO_TOKEN"))

    # Request an .xlsx file to the user to work with
    file = st.file_uploader(
        "Ingresa el billing:",
        accept_multiple_files=False,
        type=["xlsx"],
        help="Recuerda que el Excel debe seguir un formato, por lo que de nada servirá subir cualquier cosa."
    )

    # Once the user uploads the file...
    if file != None:
        # Normalize the date, removing the weekends
        date = get_date(file.name)
        
        # Instanciate the parser and execute it
        parser = BillingParser(client.get_rate(Currency.USD, date)["valor"], file=file)
        out = parser.start()
        # Set the download button with the file
        st.download_button(
            label="Descargar Excel modificado...",
            data=out,
            file_name=file.name
        )
        
        
def get_date(file_name: str) -> dt:
    """
    Gets the raw file name and extracts the date with a valid weekday
    """
    # Define a RegEx to extract the date from the name
    date_pattern = r"(\s*[A-Z]{3}\s*-\s*[0-9]{2}\s*-\s*[0-9]{2}\s*).*([0-9]{4})"
    # Search on the string and get the groups
    groups = re.search(date_pattern, file_name)
    # Split the date string
    raw_date = groups.group(1).replace(" ", "").split("-")
    # Create a datetime object based on the data
    date = dt.strptime(f"{raw_date[-1]}-{months[raw_date[0].upper()]}-{groups.group(2)}", "%d-%m-%Y")
    
    return date - td(days=shift_weekend(date.weekday()))