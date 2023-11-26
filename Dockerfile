FROM python:3.11


WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 5000

ENV NAME World

CMD ["python", "app.py"]
