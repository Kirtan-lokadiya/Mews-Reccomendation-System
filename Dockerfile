FROM python:3.11.3-slim-buster
COPY . /Newzz
WORKDIR /Newzz
EXPOSE 5000
RUN apt update -y
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
CMD  ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app", "--timeout", "90"]