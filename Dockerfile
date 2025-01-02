FROM python:alpine3.19
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt 
EXPOSE 5001
COPY . . 
CMD ["opentelemetry-instrument", "gunicorn", "--bind", "0.0.0.0:5001", "--log-level", "debug", "--timeout", "120", "main:app"]