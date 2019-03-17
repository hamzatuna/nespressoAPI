# 1) Installation and creating VirtualEnv
```
git clone https://github.com/ermissa/nespressoAPI.git
sudo apt-get install python3-venv
python3 -m venv nespresso-env
source nespresso-env/bin/activate
cd nespressoAPI/
pip install -r requirements.txt
```

create logging directory (it can be change changed from settings.py file):
```
mkdir ~/nespresso_logs
```

# 2-) Postgresql installation, Dev/Test db creation
```
sudo apt-get install postgresql postgresql-contrib
sudo -i -u postgres
psql
```
postgre change password and update settings.py
```
alter user postgres with password '1234';
```

create database
```
create database "nespressoDB";
```

create test database
```
create database postgresTestDb;
```
create tables (you can chase table changes from migrations directory)
```
python manage.py makemigrations nespressoAPI  
python manage.py migrate
```
testing application: 
```
python manage.py test
```
