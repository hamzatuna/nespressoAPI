from python:3.6.6-alpine

WORKDIR /code

COPY . .

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip3 install -r requirements.txt

CMD ["python3", "manage.py", "runserver"]