FROM python:3.12

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir --root-user-action ignore .
ENTRYPOINT ["s3daemon"]
