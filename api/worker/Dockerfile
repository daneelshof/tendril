FROM python:3.11-slim
WORKDIR /api
COPY ./requirements.txt /api/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt
COPY ./api /api
CMD ["supervisord", "-n", "-c", "/api/worker/supervisord.conf"]
