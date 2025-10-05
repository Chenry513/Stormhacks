from flask import Flask, render_template, request, jsonify
import numpy as np
import cv2
import base64
from io import BytesIO
from PIL import Image
import tensorflow as tf

app = Flask(__name__)

# Load TensorFlow Lite model
interpreter = tf.lite.Interpreter(model_path='model.tflite')
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load labels
with open('labels.txt', 'r') as f:
    labels = [line.strip() for line in f.readlines()]

def preprocess_image(image, target_size=(224, 224)):
    """Preprocess image for TensorFlow Lite model"""
    # Resize image
    image = image.resize(target_size)
    # Convert to array and normalize
    img_array = np.array(image, dtype=np.float32)
    # Normalize to [0, 1] or [-1, 1] depending on model requirements
    img_array = img_array / 255.0
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    """Classify image from webcam"""
    try:
        # Get the image data from request
        data = request.get_json()
        image_data = data['image']
        
        # Remove the data URL prefix
        image_data = image_data.split(',')[1]
        
        # Decode base64 image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes)).convert('RGB')
        
        # Preprocess image
        input_data = preprocess_image(image)
        
        # Set input tensor
        interpreter.set_tensor(input_details[0]['index'], input_data)
        
        # Run inference
        interpreter.invoke()
        
        # Get output tensor
        output_data = interpreter.get_tensor(output_details[0]['index'])
        
        # Get predictions
        predictions = output_data[0]
        
        # Create results dictionary
        results = []
        for i, label in enumerate(labels):
            results.append({
                'label': label,
                'confidence': float(predictions[i])
            })
        
        # Sort by confidence
        results = sorted(results, key=lambda x: x['confidence'], reverse=True)
        
        return jsonify({
            'success': True,
            'predictions': results
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
