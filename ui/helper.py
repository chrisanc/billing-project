# Dict to map the months to their respective integer
months: dict[str, int] = {
    "JAN": 1, "ENE": 1,
    "FEB": 2,
    "MAR": 3,
    "ABR": 4, "APR": 4,
    "MAY": 5,
    "JUN": 6,
    "JUL": 7,
    "AUG": 8, "AGO": 8,
    "SEP": 9,
    "OCT": 10,
    "NOV": 11,
    "DEC": 12, "DIC": 12
}

def shift_weekend(weekday: int) -> int:
    """
    Takes a weekday and, if it's greater than 4 (weekend),
    shifts the value to the friday
    """
    if weekday < 5:
        return 0
    
    return weekday - 4