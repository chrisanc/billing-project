import streamlit as st
from datetime import datetime as dt, timedelta as td
import re
from helper import months, shift_weekend

# UI Functionality using Streamlit.
# The goal is to create a useful, pretty and intuitive UI for users.

# Display basic information about the system
st.title("Automation")
st.text("Created by: Christian Sánchez.")

# Request an .xlsx file to the user to work with
file = st.file_uploader(
    "Ingresa el billing:",
    accept_multiple_files=False,
    type=["xlsx"],
    help="Recuerda que el Excel debe seguir un formato, por lo que de nada servirá subir cualquier cosa."
)

if file != None:
    # Define a RegEx to extract the date from the name
    date_pattern = r"(\s*[A-Z]{3}\s*-\s*[0-9]{2}\s*-\s*[0-9]{2}\s*).*([0-9]{4})"
    # Search on the string and get the groups
    groups = re.search(date_pattern, file.name)
    # Split the date string
    raw_date = groups.group(1).replace(" ", "").split("-")
    # Create a datetime object based on the data
    date = dt.strptime(f"{raw_date[-1]}-{months[raw_date[0].upper()]}-{groups.group(2)}", "%d-%m-%Y")
    # Normalize the date, removing the weekends
    date = date - td(days=shift_weekend(date.weekday()))