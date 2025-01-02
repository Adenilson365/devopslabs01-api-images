from flask import Flask, request, send_file, jsonify
import os
import logging
from flask_cors import CORS



logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

logger.handlers[0].setFormatter(logging.Formatter("time: %(asctime)s - %(levelname)s - line: %(lineno)d - file: %(filename)s - msg: %(message)s"))




app = Flask(__name__)
CORS(app)
# Diretório onde as imagens serão armazenadas no container
IMAGE_DIR = './images'
os.makedirs(IMAGE_DIR, exist_ok=True)

@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        logger.error("Nenhuma imagem enviada!")
        return jsonify({'error': 'Nenhuma imagem enviada'}), 400
    
    image = request.files['image']
    if image.filename == '':
        logger.error("Nome de arquivo Inválido")
        return jsonify({'error': 'Nome de arquivo inválido'}), 400
    
    # Salva a imagem no diretório de imagens do container
    image_path = os.path.join(IMAGE_DIR, image.filename)
    print(image_path)
    image.save(image_path)
    logger.info(f"Imagem salva com sucesso! ID: {image.filename}")
    return jsonify({'message': 'Imagem salva com sucesso', 'image_id': image.filename}), 201

@app.route('/get-image/<string:image_id>', methods=['GET'])
def get_image(image_id):
    try:
        # Busca a imagem pelo ID
        image_path = os.path.join(IMAGE_DIR, image_id)
        
        if not os.path.exists(image_path):
            logger.error(f"Imagem não encontrada! ID: {image_id}")
            return jsonify({'error': 'Imagem não encontrada'}), 404
        
        logger.info(f'Imagem encontrada: {image_id}')
        return send_file(image_path, mimetype='image/png')
    except Exception as e:
        logger.error("Erro ao carregar imagem!")
        return jsonify({'error': f'Erro ao carregar a imagem: {str(e)}'}), 500

