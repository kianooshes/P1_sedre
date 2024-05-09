FROM python:3.12
LABEL MAINTAINER="Kianoosh eskandari nezhad"

ENV PYTHONUNBUFFERED 1

RUN mkdir /store_of_book
WORKDIR /store_of_book
copy . /store_of_book

ADD requirements/requirements.txt /store_of_book
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["gunicorn", "--chdir", "store_of_book", "--bind", ":8000", "store_of_book.wsgi:application"]
