from datetime import datetime
from django.db.models import Q

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
always_true = ~Q(pk=None)

def filter_start_date(start_date):
    if start_date in ('null', None):
        return always_true
    
    date = datetime.strptime(start_date, DATE_FORMAT)
    
    return Q(date__gte=date)

def filter_end_date(end_date):
    if end_date in ('null', None):
        return always_true

    date = datetime.strptime(end_date, DATE_FORMAT)
    
    return Q(date__lte=date)

def filter_machine_id(machine_id):
    if machine_id in ('null', '', None):
        return always_true

    return Q(machine=int(machine_id))

def filter_location_id(location_id):
    if location_id in ('null', '', None):
        return always_true
    
    return Q(location=int(location_id))

def filter_personnel_name(personnel_name):
    if personnel_name in ('null', '', None):
        return always_true
    
    return Q(personnel__name__contains=personnel_name)

def filter_personnel_surname(personnel_surname):
    if personnel_surname in ('null', '', None):
        return always_true
    
    return Q(personnel__surname__contains=personnel_surname)

def filter_is_campaign(is_campaign):
    if is_campaign in ('null', '', None):
        return always_true
    
    return Q(is_campaign=bool(int(is_campaign)))

def get_sale_filters(data):
    # get post values or default values
    start_date = data.get('startdate', 'null')
    end_date = data.get('enddate', 'null')
    machine_id = data.get('machine_id', 'null')
    location_id = data.get('location_id', 'null')
    personnel_name = data.get('personnel_name', 'null')
    personnel_surname = data.get('personnel_surname', 'null')
    is_campaign = data.get('is_campaign', 'null')

    filters = [
        filter_start_date(start_date),
        filter_end_date(end_date),
        filter_machine_id(machine_id),
        filter_location_id(location_id),
        filter_personnel_name(personnel_name),
        filter_personnel_surname(personnel_surname),
        filter_is_campaign(is_campaign)
    ]

    return filters