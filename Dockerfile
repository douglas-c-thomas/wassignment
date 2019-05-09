FROM python:3
ENV PYTHONUNBUFFERED 1

ADD ./.docker/wait-for-it.sh .

ADD ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /code
ADD ./src /code
WORKDIR /code
CMD python manage.py collectstatic --no-input && python manage.py migrate && gunicorn -b :8000 wassignment.wsgi