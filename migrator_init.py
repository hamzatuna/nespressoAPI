from nespressoAPI.models import User, Machines, Locations, Personnels, Sales, Stock, StockHistory
from django.contrib.auth.hashers import make_password

# add initial admin
password_raw = "boran.1994"
password_hashed = make_password(password_raw)
test_user_data = {
    "username": "boran",
    "password": password_hashed,
    "email": "boran@nespresso.com",
    "is_active": True,
    "user_type": 1
}
User.objects.create(**test_user_data)


# add machine
test_machine_data = {
    'name': 'BEYAZ_MAKINE',
}
test_machine = Machines(**test_machine_data)
test_machine.save()

# add location
location_data = {
    "latitude": 41.0850829,
    "longitude": 29.0064543999994,
    "name": "SAFIR",
}
location = Locations(**location_data)
location.save()



# add personnel
password_raw = "12345678."
password_hashed = make_password(password_raw)
test_user_data = {
    "username": "satici0",
    "password": password_hashed,
    "email": "satici0@nespresso.com",
    "is_active": True,
    "user_type": 2
}
test_user = User(**test_user_data)
test_user.save()
test_personnel_data = {
    "user": test_user,
    "name": "satici0",
    "surname": "satici0",
    "location": location,
    "tc_no": 12345678901
}
test_personnel = Personnels(**test_personnel_data)
test_personnel.save()
