FROM python:3.10

RUN mkdir /api

WORKDIR /api

RUN pip install --upgrade pip

COPY requirements.txt /api/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /api/

EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]