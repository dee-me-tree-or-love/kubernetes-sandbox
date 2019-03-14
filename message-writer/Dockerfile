FROM python:3.7-slim

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /usr/src/app


EXPOSE 5050
CMD ["gunicorn", "-b", "0.0.0.0:5050", "--reload", "app"]