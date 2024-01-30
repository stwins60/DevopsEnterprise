FROM python:3.11

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

EXPOSE 5000


CMD ["waitress-serve", "--listen=*:5000", "app:app"]