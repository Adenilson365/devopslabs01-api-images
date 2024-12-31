FROM python:alpine3.19
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt 
EXPOSE 5001
COPY . . 

ENV OTEL_TRACES_EXPORTER=otlp
ENV OTEL_EXPORTER_OTLP_ENDPOINT=172.19.111.99:4317
ENV OTEL_RESOURCE_ATTRIBUTES=service.name=api-images
ENV OTEL_PYTHON_LOG_CORRELATION=true

CMD ["opentelemetry-instrument", "python3", "main.py"]