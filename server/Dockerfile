FROM python:3.10-alpine

WORKDIR /server

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt --verbose

COPY . /server

ENV FLASK_APP=wsgi.py

EXPOSE 5000

CMD ["waitress-serve", "--host=0.0.0.0", "--port=5000", "wsgi:app"]