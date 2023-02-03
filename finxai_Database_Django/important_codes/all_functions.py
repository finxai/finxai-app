from re import sub
from datetime import datetime

def clear_value(value):
    value = sub("[%,$N/A]", "", value.strip()) or None
    if value:
        if "." in value:
            return float(value)
        else:
            return int(value)


def clear_key(key):
    key = str(key).lower().strip()
    key = sub("[%,$&'-]", "", key)
    key = sub("\s\s+", " ", key)
    key = key.replace(" ", "_").replace("-", "_")
    return key or None


def convert_string_to_date(value, input):
    if value == "" or value == "-" or value == "N/A" or value == None:
        return None
    else:
        return (datetime.strptime(value, input)).strftime("%Y-%m-%d")