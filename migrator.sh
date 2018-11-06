#echo "pulling current branch"
#git pull


#  drop and create database
#  from
#  https://stackoverflow.com/questions/13419214/drop-db-in-postgres
echo "dropping database nespressoDB"
sudo -u postgres psql -c 'DROP DATABASE "nespressoDB"'

echo "creating database nespressoDB"
sudo -u postgres psql -c 'CREATE DATABASE "nespressoDB"'

echo "creating migrations folder"
rm -r nespressoAPI/migrations/
mkdir nespressoAPI/migrations

echo "making migrations"
python manage.py makemigrations nespressoAPI
python manage.py migrate


#  add first admin (boran, boran.1994)
#  add first machine (BEYAZ_MAKINE)
#  add first location (SAFIR)
echo "creating dummy database objects"
python manage.py shell -c "$(cat migrator_init.py)"


#  TO DO
#  restart gunicorn
