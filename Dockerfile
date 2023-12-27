FROM python:3.12.0-slim

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

RUN pip3 install --upgrade pip

COPY requirements.txt /code/

RUN pip3 install --no-cache-dir --upgrade pip

RUN pip3 install -r requirements.txt

COPY . /code/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]