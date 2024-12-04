from flask import Flask, request, send_file, jsonify
import os
from flask_cors import CORS;


app = Flask(__name__)
CORS(app )
# Diretório onde as imagens serão armazenadas no container
IMAGE_DIR = './images'
os.makedirs(IMAGE_DIR, exist_ok=True)

@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'Nenhuma imagem enviada'}), 400
    
    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'Nome de arquivo inválido'}), 400
    
    # Salva a imagem no diretório de imagens do container
    image_path = os.path.join(IMAGE_DIR, image.filename)
    print(image_path)
    image.save(image_path)
    
    return jsonify({'message': 'Imagem salva com sucesso', 'image_id': image.filename}), 201

@app.route('/get-image/<string:image_id>', methods=['GET'])
def get_image(image_id):
    try:
        # Busca a imagem pelo ID
        image_path = os.path.join(IMAGE_DIR, image_id)
        print(image_path)
        if not os.path.exists(image_path):
            return jsonify({'error': 'Imagem não encontrada'}), 404
        return send_file(image_path, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': f'Erro ao carregar a imagem: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
