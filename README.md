# 1) Kurulum ve VirtualEnv Olusturma
```
git clone https://github.com/ermissa/nespressoAPI.git
sudo apt-get install python3-venv
python3 -m venv nespresso-env
source nespresso-env/bin/activate
cd nespressoAPI/
pip install -r requirements.txt
```

# 2-) Postgresql Kurulumu, Dev/Test db olusturulmasi
```
sudo apt-get install postgresql postgresql-contrib
sudo -i -u postgres
psql
```
postgre terminalinde sifre degistirme
```
alter user postgres with password '1234';
```
test database olusturma
```
create database postgresTestDb;
```
tablolari olusturma
```
 python manage.py makemigrations nespressoAPI
 python manage.py migrate
 ```
 test etme: 
 ```
 python manage.py test
 ```