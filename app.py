import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import cv2
import uuid

from detector import ObjectDetector
from enhancement import enhance_low_light_image

app = Flask(__name__)
# Enable CORS for React frontend (running on a different port like 5173)
CORS(app)

# Configuration keys
UPLOAD_FOLDER = 'outputs/web_uploads'
PROCESSED_FOLDER = 'outputs/web_processed'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Initialize detector globally
print("Initializing backend detector instance...")
detector = ObjectDetector()
print("Backend detector initialized.")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    # 1. Check if file is in request
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if file and allowed_file(file.filename):
        # 2. Save the original uploaded file securely
        ext = file.filename.rsplit('.', 1)[1].lower()
        unique_id = str(uuid.uuid4())
        filename = f"{unique_id}.{ext}"
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # 3. Process the file (Read -> Enhance -> Detect)
        image = cv2.imread(filepath)
        if image is None:
            return jsonify({"error": "Invalid image file"}), 400
            
        # Enhance
        enhanced_image = enhance_low_light_image(image, use_gamma=True, use_clahe=True, gamma_val=0.5)
        enhanced_filename = f"enhanced_{filename}"
        enhanced_filepath = os.path.join(app.config['PROCESSED_FOLDER'], enhanced_filename)
        cv2.imwrite(enhanced_filepath, enhanced_image)
        
        # Detect
        detected_image, _ = detector.detect(enhanced_image)
        detected_filename = f"detected_{filename}"
        detected_filepath = os.path.join(app.config['PROCESSED_FOLDER'], detected_filename)
        cv2.imwrite(detected_filepath, detected_image)
        
        # 4. Return the URLs to access the processed items
        return jsonify({
            "original_url": f"/images/uploads/{filename}",
            "enhanced_url": f"/images/processed/{enhanced_filename}",
            "detected_url": f"/images/processed/{detected_filename}"
        }), 200
        
    return jsonify({"error": "File type not allowed"}), 400

# Endpoint to serve the actual images
@app.route('/images/uploads/<filename>', methods=['GET'])
def get_uploaded_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/images/processed/<filename>', methods=['GET'])
def get_processed_image(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

if __name__ == '__main__':
    # Run the server
    app.run(host='0.0.0.0', port=5001, debug=True)
