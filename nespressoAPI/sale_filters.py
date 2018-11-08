from datetime import datetime
from django.db.models import Q

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

def filter_start_date(start_date):
    date = datetime.strptime(start_date, DATE_FORMAT)
    
    return Q(date__gte=date)