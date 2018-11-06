from nespressoAPI.models import User, Machines, Locations, Personnels, Sales, Stock, StockHistory


# add initial admin
password_raw = "boran.1994"
password_hashed = make_password(password)
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
    'id': 1,
    'name': 'BEYAZ_MAKINE',
}
test_machine = Machines(**test_machine_data)
test_machine.save()

# add location
location_data = {
    "id": 1,
    "latitude": 45.1,
    "longitude": 34.12,
    "name": "SAFIR",
}
location = Locations(**location_data)
location.save()
