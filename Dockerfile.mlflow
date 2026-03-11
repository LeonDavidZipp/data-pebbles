FROM ghcr.io/mlflow/mlflow:v3.8.0rc0

ENV PYTHONUNBUFFERED=1
ENV MLFLOW_S3_ENDPOINT_URL=""
ENV MLFLOW_S3_IGNORE_TLS=""
ENV AWS_ACCESS_KEY_ID=""
ENV AWS_SECRET_ACCESS_KEY=""

WORKDIR /app
RUN pip install --no-cache-dir \
    boto3 \
    psycopg2-binary


EXPOSE 5000

CMD mlflow server \
    --backend-store-uri postgresql+psycopg2://${AWS_ACCESS_KEY_ID}:${AWS_SECRET_ACCESS_KEY}@postgres/mlflow \
    --default-artifact-root s3://mlflow/ \
    --artifacts-destination s3://mlflow/ \
    -h 0.0.0.0