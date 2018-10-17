# Kullanici islemleri
## 1-) Kullanici Islemleri

```
/register POST
```
body ornek:
```
{
    "username": "test2",
    "password": "test2",
    "email": "test2@test.com",
    "is_active": true,
    "user_type": 1
}
```

```
/register POST
```
body ornek:
```
{
    "name": "test-name",
    "wage": null,
    "phone_number": null,
    "user": {
        "username": "test-user-name5",
        "email": "a5@a.com",
        "is_active": true,
        "user_type": 1
    },
    "location_id": 1
}
```
## 2-) Token Alma

```
/get-token POST
```
body ornek:
```
{
    "username": "test2",
    "password": "test2",
}
```
Sonuc:
```
{
    "token": "feb077537b9225af583b1c10b31dda77d88379a5"
}
```

## 3-) Personel ekleme

```
/register/personnel POST
```
authtication olmak icin header`a:
```
"Authorization: Token 241389a7b0e2f30668f8e71ce2bdff9a4a47d5c3(giriste alinan token)"
```
body ornek:
```
{
   "user": {
	"username": "test6",
	"password": "12345678.",
	"email": "a7@a.com",
	"is_active": true,
	"user_type": 1
   },
   
   "name": "test-name1",
   "surname": "test-surname",
   "email": "a1@a.com"
}
```
Sonuc: olusturulan personel bilgileri doner
```
{
   "user": {
	"username": "test6",
	"email": "a7@a.com",
	"is_active": true,
	"user_type": 1
   },
   
   "name": "test-name1",
   "surname": "test-surname",
   "email": "a1@a.com"
}
```

# Endpoitlere Permission ekleme

fonksiyona ekleme:
```
@manager_required
@api_view(['GET'])
def get_sales_count(request):
```
class`a ekleme:
```
class RegisterPersonnel(CreateAPIView):
    serializer_class = PersonnelSerializer
    queryset = Personnels.objects.all()
    permission_classes = (IsManeger,)
```