FROM python:3.10-alpine

WORKDIR /admin

COPY . /admin

ENV FLASK_APP=app.py

EXPOSE 5001

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "app:app"]