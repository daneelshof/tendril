FROM python:3.11-slim
WORKDIR /api
COPY ./requirements.txt /api/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt
COPY ./api /api
CMD ["uvicorn", "main:api", "--host", "0.0.0.0", "--port", "80", "--log-config", "logging_config.yml"]

