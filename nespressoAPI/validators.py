import re

# validators
def month_validator(dt): 
    return re.match(r'\d{4}-\d{2}-01 00:00:00', dt.strftime("%Y-%m-%d %H:%M:%S"))