FROM registry.sedrehgroup.ir/python:3.8
LABEL MAINTAINER="Kianoosh eskandari nezhad"

ENV PYTHONUNBUFFERED 1

RUN mkdir /store_of_book
WORKDIR /store_of_book

COPY . /store_of_book

RUN pip install --upgrade pip
RUN pip install -r /store_of_book/requirements/requirements.txt

CMD ["gunicorn", "--chdir", "store_of_book", "--bind", "0.0.0.0:8000", "store_of_book.wsgi:application"]
