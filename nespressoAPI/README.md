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
makine boyle eklenicek


## 5-) Satış Ekleme

```
/sales POST
```
body ornek:
Satis eklemeden once personel icin lokasyon tanimlanmis olmasi lazimdir ve lokasyona ait bir de makine olmasi lazimdir
```       
{
	"personnel_id": 4,
	"CustomerName": "testName",
	"CustomerSurname": "CustomerSurname",
	"CustomerPhoneNumber": "23233232323",
	"CustomerEmail": "aawdaw@a.com",
    "MachineId": 1,
	"IsCampaign": true
}
```
Sonuc:
```
{
    "id": 14,
    "Date": "2018-09-10T01:32:12.922000Z",
    "CustomerName": "YEPSYENI7",
    "CustomerSurname": "ADAM7",
    "CustomerPhoneNumber": "05672348294",
    "CustomerEmail": "ADAMLIQUE7@gmail.com",
    "IsCampaign": false,
    "MachineId": 1,
    "personnel_id": 4,
    "location_id": 1
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
    "machine": 1,
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
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "stock_count": 5,
            "machine": 1,
            "location": 1
        },
        {
            "id": 2,
            "stock_count": 5,
            "machine": 1,
            "location": 1
        },
        {
            "id": 4,
            "stock_count": 5,
            "machine": 1,
            "location": 1
        }
    ]
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
