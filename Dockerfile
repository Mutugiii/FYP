FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

RUN apk update && \
    apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
ADD requirements.txt /app/
RUN pip install -r requirements.txt

COPY ./ /app/

CMD ["python", "manage.py", "runserver"]
