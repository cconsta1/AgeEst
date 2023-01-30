FROM python:3.10

# EXPOSE 8050

WORKDIR /app

COPY . .
COPY models /app/models/

RUN pip install -r requirements.txt

EXPOSE 8050

CMD ["gunicorn", "-b", "0.0.0.0:8050", "--reload", "app:server"]