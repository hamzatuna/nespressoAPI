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
    "password": "test2"
}
```
Sonuc:
```
{
    "token": "feb077537b9225af583b1c10b31dda77d88379a5"
    "id": 1,
    "user_type": 1
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
   "location_id":1,
   "name": "test-name1",
   "surname": "test-surname",
   "email": "a1@a.com",
   "tc_no": 12345678901
}
```
Sonuc: olusturulan personel bilgileri doner
```
{
    "name": "test-name1",
    "wage": null,
    "phone_number": null,
    "user": {
        "username": "test6",
        "email": "a7@a.com",
        "is_active": true,
        "user_type": 2
    },
    "location_id": null
}
```

## 4-) Makine Ekleme

```
/get_machines POST
```
Headerda Authorization/Token olmasi gerekli.

body ornek:
```
{
    "name": "BEYAZ_MAKINE"
}
```
Sonuc: olusturulan makine bilgileri doner
```
{
    "id": 1,
    "name": "BEYAZ_MAKINE"
}
```


## 5-) Satış Ekleme

```
/sales POST
```
body ornek:
Satis eklemeden once personel icin lokasyon tanimlanmis olmasi lazimdir ve lokasyona ait bir de makine olmasi lazimdir
```       
{
    "customer_name": "testName",
    "customer_surname": "customer_surname",
    "customer_phone_number": "23233232323",
    "customer_email": "aawdaw@a.com",
    "latitude": 45.1,
    "longitude": 45.2,
    "price": "23.000",
    "serial_number": "aweawe",
    "is_campaign": true,
	"machine": 1,
	"personnel": 2
}
```
Sonuc:
```
{
    "customer_name": "testName",
    "customer_surname": "customer_surname",
    "customer_phone_number": "23233232323",
    "customer_email": "aawdaw@a.com",
    "latitude": 45.1,
    "longitude": 45.2,
    "price": "23.000",
    "serial_number": "aweawe",
    "is_campaign": true,
	"machine": 1,
	"personnel": 2
}
```


## 6-) Hedef Ekleme

```
/goals POST
```
body ornek:

```       
{
    "sale_goal": 1,
    "date": "2018-01-02",
    "user": 1
}
```
birden fazla eklemek icin liste olarak gonderilmesi yeterlidir:
```       
[
    {
        "sale_goal": 1,
        "date": "2018-01-02",
        "user": 1
    }
]
```
Sonuc:
```
{
    "id": 2,
    "sale_goal": 1,
    "date": "2018-01-02",
    "user": 1
}
```
## 7-) Hedef Updateleme

```
/goals/<id>/ PATCH
```
body ornek:

```       
{
    "sale_goal": 1,

}
```

Sonuc:
```
{
    "id": 2,
    "sale_goal": 1,
    "date": "2018-01-02",
    "user": 1
}
```



## 8-) Stock Ekleme

```
/stocks POST
```
body ornek:

```       
{
    "id": 4,
    "stock_count": 5,
    "machine_id": 1,
    "location": 1
}
```
Sonuc:
```
{
    "id": 4,
    "stock_count": 5,
    "machine": 1,
    "location": 1
}
```

## 9-) Stock Cekme

```
/stocks GET
```
Istegin yapan kullanici personnelse personel lokasyonundakileri doner, Eger kullanici tipi managerse butun stoklari doner. 
Sonuc:
```
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "machine": {
                "id": 1,
                "name": "awe"
            },
            "stock_count": 3,
            "location": 1
        }
    ]
}
```

## 9-) Personnel Lokasyon Degistirme

```
/personnel/update/2(personnelin idsi)/ Patch
```
Body:
```
{
    'location_id': 2
}
```
Sonuc:
```
{
    "user": {
        "username": "test_personel5",
        "email": "aeaea3543@a.com",
        "is_active": true,
        "user_type": 2
    },
    "location": {
        "id": 2,
        "latitude": 35,
        "longitude": 35,
        "name": "test2"
    },
    "name": "test-name1",
    "surname": "test-surname",
    "birthday": "1994-01-02",
    "phone_number": null,
    "wage": null,
    "tc_no": 12345678901
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
    serializer_class = PersonnelsSerializer
    queryset = Personnels.objects.all()
    permission_classes = (IsManager,)
```
