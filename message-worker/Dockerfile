FROM python:3.7-slim

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt

# RUN pip install repyt

COPY . /usr/src/app

# CMD ["repyt", "app.py"]
CMD ["python", "app.py"]