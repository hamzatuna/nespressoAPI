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
    "location_id": null
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