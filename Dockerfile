FROM python:slim-buster

WORKDIR /app

COPY ./requirements.txt /app

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8125

CMD ["gunicorn", "-b", "0.0.0.0:8125", "--log-level", "debug", "app:app"]
