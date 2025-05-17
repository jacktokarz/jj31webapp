FROM python:3.10

RUN mkdir /bot

WORKDIR /bot

RUN pip install --upgrade pip

COPY ./requirements.txt /bot/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /bot/

EXPOSE 4243