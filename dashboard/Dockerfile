FROM python:3.11-slim
WORKDIR /dashboard
COPY ./dashboard/requirements.txt /dashboard/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /dashboard/requirements.txt
CMD ["rq-dashboard", "-u", "redis://redis:6379"]