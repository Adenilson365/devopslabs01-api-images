from flask import Flask, request, send_file, jsonify
import os
import logging
from flask_cors import CORS;

from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

provider = TracerProvider(resource=Resource.create({SERVICE_NAME: "api-images"}))
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
resource = Resource(attributes={
    SERVICE_NAME: "api-images"
})
# Sets the global default tracer provider
trace.set_tracer_provider(provider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer("my.tracer.name")

otlp_exporter = OTLPSpanExporter(
    endpoint="http://opentelemetry-collector.obs.svc.cluster.local:4318/v1/traces",  # Ajuste conforme IP/porta do Collector
    # headers={"Authorization": "Bearer <token>"},  # se necessário
)

def do_work():
    with tracer.start_as_current_span("work") as span:
        # do some work that 'span' will track
        span.set_attribute("name", "teste")
        print("doing some work...")
        # When the 'with' block goes out of scope, 'span' is closed for you


logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(asctime)s - %(message)s')

app = Flask(__name__)
CORS(app )
# Diretório onde as imagens serão armazenadas no container
IMAGE_DIR = './images'
os.makedirs(IMAGE_DIR, exist_ok=True)

@app.route('/upload-image', methods=['POST'])
def upload_image():
    do_work()
    if 'image' not in request.files:
        logging.error("Nenhuma imagem enviada")
        return jsonify({'error': 'Nenhuma imagem enviada'}), 400
    
    image = request.files['image']
    if image.filename == '':
        logging.error("Nome de arquivo Inválido")
        return jsonify({'error': 'Nome de arquivo inválido'}), 400
    
    # Salva a imagem no diretório de imagens do container
    image_path = os.path.join(IMAGE_DIR, image.filename)
    print(image_path)
    image.save(image_path)
    logging.info("Imagem salva com sucesso")
    return jsonify({'message': 'Imagem salva com sucesso', 'image_id': image.filename}), 201

@app.route('/get-image/<string:image_id>', methods=['GET'])
def get_image(image_id):
    do_work()
    try:
        # Busca a imagem pelo ID
        image_path = os.path.join(IMAGE_DIR, image_id)
        print(image_path)
        if not os.path.exists(image_path):
            logging.error("Imagem não encontrada")
            return jsonify({'error': 'Imagem não encontrada'}), 404
        return send_file(image_path, mimetype='image/png')
    except Exception as e:
        logging.error("Erro ao carregar imagem")
        return jsonify({'error': f'Erro ao carregar a imagem: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
