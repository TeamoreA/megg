FROM python:latest

LABEL MAINTAINER 'Teamore'

LABEL APPLICATION 'Project Megg'

RUN apt update && pip install --upgrade pip

# COPY src /src

# COPY env /env

COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

WORKDIR /src

EXPOSE 8000

ENTRYPOINT [ "./manage.py", "runserver", "0.0.0.0:8000" ]