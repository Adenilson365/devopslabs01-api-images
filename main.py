from flask import Flask, request, send_file, jsonify
import os
import logging
from flask_cors import CORS
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.opencensus.trace_exporter import OpenCensusSpanExporter
from opentelemetry.sdk.resources import Resource

# Configuração do OpenTelemetry
resource = Resource(attributes={
    "service.name": "image-api",
    "service.version": "1.0.0"
})

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# Exportador OpenCensus para spans
exporter = OpenCensusSpanExporter(service_name="image-api")
span_processor = BatchSpanProcessor(exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(asctime)s - %(message)s')

# Criação da aplicação Flask
app = Flask(__name__)
CORS(app)

# Instrumentação automática do Flask
FlaskInstrumentor().instrument_app(app)

# Adicionar middleware para suporte ao WSGI
app.wsgi_app = OpenTelemetryMiddleware(app.wsgi_app)

# Diretório onde as imagens serão armazenadas no container
IMAGE_DIR = './images'
os.makedirs(IMAGE_DIR, exist_ok=True)

@app.route('/upload-image', methods=['POST'])
def upload_image():
    with tracer.start_as_current_span("upload_image"):
        if 'image' not in request.files:
            logging.error("Nenhuma imagem enviada")
            return jsonify({'error': 'Nenhuma imagem enviada'}), 400
        
        image = request.files['image']
        if image.filename == '':
            logging.error("Nome de arquivo Inválido")
            return jsonify({'error': 'Nome de arquivo inválido'}), 400
        
        # Salva a imagem no diretório de imagens do container
        image_path = os.path.join(IMAGE_DIR, image.filename)
        image.save(image_path)
        logging.info("Imagem salva com sucesso")
        return jsonify({'message': 'Imagem salva com sucesso', 'image_id': image.filename}), 201

@app.route('/get-image/<string:image_id>', methods=['GET'])
def get_image(image_id):
    with tracer.start_as_current_span("get_image"):
        try:
            # Busca a imagem pelo ID
            image_path = os.path.join(IMAGE_DIR, image_id)
            if not os.path.exists(image_path):
                logging.error("Imagem não encontrada")
                return jsonify({'error': 'Imagem não encontrada'}), 404
            return send_file(image_path, mimetype='image/png')
        except Exception as e:
            logging.error("Erro ao carregar imagem")
            return jsonify({'error': f'Erro ao carregar a imagem: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
