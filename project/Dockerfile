FROM python:3.8.8-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1 # Prevents Python from writing pyc files to disc
ENV PYTHONUNBUFFERED 1 # Prevents Python from buffering stdout and stderr


RUN apt-get update && \
    apt-get -y install netcat gcc && \
    apt-get clean

# install python dependencies
COPY Pipfile Pipfile.lock ./
RUN apt-get update && \
    apt-get -qy full-upgrade && \
    apt-get install -qy curl && \
    curl -sSL https://get.docker.com/ | sh

RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --dev --ignore-pipfile --deploy --system

# add app
COPY . .

# add entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
