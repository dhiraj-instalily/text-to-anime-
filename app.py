from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from call_model import generate_image
import os

app = Flask(__name__, static_folder='image-generator-frontend/build', static_url_path='')
CORS(app)  # Enable CORS for all routes

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# Serve generated images
@app.route('/generated/<path:filename>')
def serve_generated_image(filename):
    return send_from_directory('static', filename)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt', '')
    negative_prompt = data.get('negative_prompt', '')
    
    image_path = generate_image(prompt, negative_prompt)
    
    # Return the URL path to the image
    return jsonify({'image_path': f'/generated/{os.path.basename(image_path)}'})

if __name__ == '__main__':
    app.run(debug=True)