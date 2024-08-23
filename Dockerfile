FROM python:3.11

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/softproapp

WORKDIR /softproapp

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY soft_pro .

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh