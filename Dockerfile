FROM python:3.11.3-slim-buster
COPY . /WineQualityApp
WORKDIR /WineQualityApp
EXPOSE 8000
RUN apt update -y
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
# CMD  will give after designing the front