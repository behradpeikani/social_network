FROM python:latest

WORKDIR /src

COPY requirements.txt /src/

RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . /src

EXPOSE 8000

CMD ["gunicorn", "core.wsgi", ":8000"]