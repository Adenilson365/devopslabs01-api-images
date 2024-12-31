FROM python:alpine3.19
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir opentelemetry-instrument \
    opentelemetry-exporter-otlp
RUN pip3 install --no-cache-dir -r requirements.txt 
EXPOSE 5001
ENV OTEL_EXPORTER_OTLP_ENDPOINT=http://opentelemetry-collector.obs.svc.cluster.local:4318 \
    OTEL_METRICS_ENABLED=true \
    OTEL_TRACES_ENABLED=true
COPY . . 
CMD ["opentelemetry-instrument","python3", "main.py"]