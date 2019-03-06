FROM python:3.7-slim

WORKDIR /usr/src/app

ENV FLASK_DEBUG=development
ENV FLASK_APP=app.py

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /usr/src/app

EXPOSE 5000
CMD ["python", "-m", "flask", "run"]